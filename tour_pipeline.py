#!/usr/bin/env python3
"""
TourPipeline: A deep, consolidated module for rendering the 100% artifact-free
FPV drone scrollytelling tour of the resort.

Encapsulates asset cataloging, camera kinematics, door/curtain perspective
transformations, video encoding, and high-performance WebP frame extraction.
"""

from dataclasses import dataclass
import math
import os
import sys
import argparse
from typing import Optional, Callable
import cv2
import numpy as np


@dataclass
class TourConfig:
    width: int = 1920
    height: int = 1080
    fps: int = 30
    total_frames: int = 600
    asset_dir: str = "img"
    video_output: str = "resort_drone_flight.mp4"
    frames_dir: str = "frames_webp"
    webp_quality: int = 80


class AssetCatalog:
    """Loads and pre-processes all high-res photography assets."""

    def __init__(self, asset_dir: str = "img", width: int = 1920, height: int = 1080):
        self.asset_dir = asset_dir
        self.width = width
        self.height = height

        # Load raw assets
        self.img_main1 = self._load_img("main1.jpg")
        self.img_main2 = self._load_img("main2.jpg")
        self.img_door_l = self._load_img("door_left.png")
        self.img_door_r = self._load_img("door_right.png")
        self.img_curt_l = self._load_or_create_curtain("left")
        self.img_curt_r = self._load_or_create_curtain("right")
        self.img_banq1 = self._load_img("banq1.jpg")
        self.img_banq2 = self._load_img("banq2.jpg")
        self.img_banq3 = self._load_img("banq3.jpg")
        self.img_banq4 = self._load_img("banq4.jpg")

        # Build seamless master facade panorama
        self.pano = self._build_master_facade()
        self.pano_h, self.pano_w = self.pano.shape[:2]

        # Calculate entrance door landmarks on panorama
        self.door_x1 = int(648 * 1920 / 1376)
        self.door_x2 = int(728 * 1920 / 1376)
        self.door_y1 = int(806 * 1920 / 1376)
        self.door_y2 = int(892 * 1920 / 1376)

        # Calculate right picture-window landmarks on panorama
        self.win_x1 = int(770 * 1920 / 1376)
        self.win_x2 = int(840 * 1920 / 1376)
        self.win_y1 = int(792 * 1920 / 1376)
        self.win_y2 = int(892 * 1920 / 1376)

        # Pre-scale interior assets for aspect cover
        self.asset_banq1 = self._make_cover_asset(self.img_banq1)
        self.asset_banq2 = self._make_cover_asset(self.img_banq2)
        self.asset_banq3 = self._make_cover_asset(self.img_banq3)
        self.asset_banq4 = self._make_cover_asset(self.img_banq4)

    def _load_img(self, filename: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
        path = os.path.join(self.asset_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required asset not found: {path}")
        img = cv2.imread(path, flags)
        if img is None:
            raise ValueError(f"Failed to decode image: {path}")
        return img

    def _load_or_create_curtain(self, side: str) -> np.ndarray:
        path = os.path.join(self.asset_dir, f"curtain_{side}.png")
        if os.path.exists(path):
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                return img
        # Synthesize realistic semi-transparent sheer curtain
        h, w = 600, 300
        curt = np.zeros((h, w, 4), dtype=np.uint8)
        curt[:, :, 0] = 230  # B (warm ivory)
        curt[:, :, 1] = 242  # G
        curt[:, :, 2] = 252  # R
        for x in range(w):
            phase = 0.0 if side == "left" else math.pi
            fold = 0.65 + 0.25 * math.sin(x * 0.09 + phase) + 0.10 * math.cos(x * 0.04)
            edge = 1.0 - (x / float(w) * 0.3) if side == "left" else 0.7 + (x / float(w) * 0.3)
            alpha = np.clip(180 * fold * edge, 70, 230)
            curt[:, x, 3] = int(alpha)
        cv2.imwrite(path, curt)
        return curt

    def _build_master_facade(self) -> np.ndarray:
        w_raw = self.img_main1.shape[1]
        m2 = (
            cv2.resize(self.img_main2, (w_raw, self.img_main2.shape[0]))
            if self.img_main2.shape[1] != w_raw
            else self.img_main2
        )
        m1_h = self.img_main1.shape[0]
        m2_h = m2.shape[0]
        overlap_h = 456
        total_h = m1_h + m2_h - overlap_h

        pano_raw = np.zeros((total_h, w_raw, 3), dtype=np.uint8)
        pano_raw[0 : m1_h - overlap_h, :] = self.img_main1[0 : m1_h - overlap_h, :]

        alpha = np.linspace(0, 1, overlap_h)[:, None, None].astype(np.float32)
        pano_raw[m1_h - overlap_h : m1_h, :] = (
            self.img_main1[m1_h - overlap_h : m1_h, :].astype(np.float32) * (1.0 - alpha)
            + m2[0:overlap_h, :].astype(np.float32) * alpha
        ).astype(np.uint8)

        pano_raw[m1_h:total_h, :] = m2[overlap_h:, :]

        pano = cv2.resize(
            pano_raw, (1920, int(total_h * 1920 / w_raw)), interpolation=cv2.INTER_LANCZOS4
        )
        return pano

    def _make_cover_asset(self, raw_img: np.ndarray) -> np.ndarray:
        rh, rw = raw_img.shape[:2]
        scale = max(float(self.width) / rw, float(self.height) / rh)
        return cv2.resize(
            raw_img, (int(rw * scale), int(rh * scale)), interpolation=cv2.INTER_LANCZOS4
        )


class CameraEngine:
    """Evaluates smooth camera transformations strictly within image boundaries."""

    @staticmethod
    def smoothstep(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def ease_in_out(t: float) -> float:
        t = max(0.0, min(1.0, t))
        return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t

    @staticmethod
    def sample_virtual_cam(
        src: np.ndarray,
        center_x: float,
        center_y: float,
        zoom: float = 1.0,
        roll_deg: float = 0.0,
        out_w: int = 1920,
        out_h: int = 1080,
    ) -> np.ndarray:
        sh, sw = src.shape[:2]
        vw = out_w / max(0.001, zoom)
        vh = out_h / max(0.001, zoom)

        half_vw = vw / 2.0
        half_vh = vh / 2.0

        cx = max(half_vw, min(sw - half_vw, center_x))
        cy = max(half_vh, min(sh - half_vh, center_y))

        m = cv2.getRotationMatrix2D((cx, cy), roll_deg, zoom)
        m[0, 2] += (out_w / 2.0) - cx * zoom
        m[1, 2] += (out_h / 2.0) - cy * zoom

        return cv2.warpAffine(
            src,
            m,
            (out_w, out_h),
            flags=cv2.INTER_LANCZOS4,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @staticmethod
    def render_doors_and_curtains(
        pano_base: np.ndarray,
        catalog: AssetCatalog,
        door_angle: float,
        curtain_part: float,
        curtain_alpha: float,
    ) -> np.ndarray:
        f = pano_base.copy()

        # 3D Double Doors
        if door_angle > 1.0:
            cv2.rectangle(
                f,
                (catalog.door_x1, catalog.door_y1),
                (catalog.door_x2, catalog.door_y2),
                (65, 160, 245),
                -1,
            )
            roi = f[catalog.door_y1:catalog.door_y2, catalog.door_x1:catalog.door_x2].astype(
                np.float32
            )
            f[catalog.door_y1:catalog.door_y2, catalog.door_x1:catalog.door_x2] = np.clip(
                roi * 0.3 + np.array([40, 185, 255]) * 0.7, 0, 255
            ).astype(np.uint8)

            rad = math.radians(min(80.0, door_angle))
            wf = max(0.08, math.cos(rad))
            dh = catalog.door_y2 - catalog.door_y1
            dw = (catalog.door_x2 - catalog.door_x1) // 2
            dl = cv2.resize(catalog.img_door_l, (max(3, int(dw * wf)), dh))
            dr = cv2.resize(catalog.img_door_r, (max(3, int(dw * wf)), dh))

            f[catalog.door_y1:catalog.door_y2, catalog.door_x1:catalog.door_x1 + dl.shape[1]] = dl
            f[catalog.door_y1:catalog.door_y2, catalog.door_x2 - dr.shape[1]:catalog.door_x2] = dr

        # Sheer Curtains on Right Window
        if curtain_alpha > 0.02:
            ww = catalog.win_x2 - catalog.win_x1
            wh = catalog.win_y2 - catalog.win_y1
            cw = int(ww * 0.65)
            cl_res = cv2.resize(catalog.img_curt_l, (cw, wh))
            cr_res = cv2.resize(catalog.img_curt_r, (cw, wh))
            part_px = int(curtain_part * ww * 0.60)

            # Left curtain
            lx1 = max(catalog.win_x1, catalog.win_x1 - part_px)
            lx2 = min(catalog.win_x2, catalog.win_x1 - part_px + cw)
            if lx2 > lx1:
                w_act = lx2 - lx1
                roi = f[catalog.win_y1:catalog.win_y2, lx1:lx2].astype(np.float32)
                c_rgb = cl_res[:, :w_act, :3].astype(np.float32)
                c_a = (cl_res[:, :w_act, 3].astype(np.float32) / 255.0) * curtain_alpha
                f[catalog.win_y1:catalog.win_y2, lx1:lx2] = np.clip(
                    roi * (1.0 - c_a[:, :, None]) + c_rgb * c_a[:, :, None], 0, 255
                ).astype(np.uint8)

            # Right curtain
            rx1 = max(catalog.win_x1, catalog.win_x2 + part_px - cw)
            rx2 = min(catalog.win_x2, catalog.win_x2 + part_px)
            if rx2 > rx1:
                w_act = rx2 - rx1
                roi = f[catalog.win_y1:catalog.win_y2, rx1:rx2].astype(np.float32)
                c_rgb = cr_res[:, -w_act:, :3].astype(np.float32)
                c_a = (cr_res[:, -w_act:, 3].astype(np.float32) / 255.0) * curtain_alpha
                f[catalog.win_y1:catalog.win_y2, rx1:rx2] = np.clip(
                    roi * (1.0 - c_a[:, :, None]) + c_rgb * c_a[:, :, None], 0, 255
                ).astype(np.uint8)

        return f


class TourPipeline:
    """Deep module orchestrating the 6-phase continuous FPV drone tour."""

    def __init__(self, config: Optional[TourConfig] = None):
        self.config = config or TourConfig()
        self.catalog = AssetCatalog(
            self.config.asset_dir, self.config.width, self.config.height
        )
        self.cam = CameraEngine()

    def render_frame(self, f: int) -> np.ndarray:
        """Renders an individual frame by index (0 to total_frames - 1)."""
        w, h = self.config.width, self.config.height

        # Phase 1: [0 to 140] Sky to facade descent
        if f <= 140:
            t = f / 140.0
            st = self.cam.smoothstep(t)
            cy = 540.0 + st * 420.0
            cx = self.catalog.pano_w / 2.0
            zoom = 1.0 + st * 0.25
            roll = math.sin(t * math.pi * 2.0) * 0.4

            frame_src = self.cam.render_doors_and_curtains(
                self.catalog.pano, self.catalog, 0.0, 0.0, 1.0
            )
            return self.cam.sample_virtual_cam(frame_src, cx, cy, zoom, roll, w, h)

        # Phase 2: [140 to 240] Courtyard glide, doors open, right window approach
        elif f <= 240:
            t = (f - 140) / 100.0
            st = self.cam.smoothstep(t)
            door_t = self.cam.smoothstep(min(1.0, (f - 140) / 55.0))
            door_angle = door_t * 80.0
            curtain_part = st * 0.85
            curtain_alpha = 1.0 - self.cam.smoothstep(max(0.0, (f - 200) / 40.0))

            win_cx = (self.catalog.win_x1 + self.catalog.win_x2) / 2.0
            win_cy = (self.catalog.win_y1 + self.catalog.win_y2) / 2.0

            cx = (self.catalog.pano_w / 2.0) * (1.0 - st) + win_cx * st
            cy = 960.0 * (1.0 - st) + win_cy * st
            zoom = 1.25 + st * 2.2
            roll = math.sin(t * math.pi) * 0.6

            frame_src = self.cam.render_doors_and_curtains(
                self.catalog.pano, self.catalog, door_angle, curtain_part, curtain_alpha
            )
            return self.cam.sample_virtual_cam(frame_src, cx, cy, zoom, roll, w, h)

        # Phase 3: [240 to 330] Penetrating window & entering floral corridor (banq1)
        elif f <= 330:
            t = (f - 240) / 90.0
            trans_t = self.cam.smoothstep(min(1.0, (f - 240) / 30.0))

            b1_w, b1_h = self.catalog.asset_banq1.shape[1], self.catalog.asset_banq1.shape[0]
            push1 = self.cam.ease_in_out(t)
            cx1 = (b1_w / 2.0) + self.cam.smoothstep(max(0.0, (f - 280) / 50.0)) * 120.0
            cy1 = b1_h / 2.0
            zoom1 = 1.02 + push1 * 0.45
            roll1 = math.sin(t * math.pi * 1.5) * 0.5

            cam1 = self.cam.sample_virtual_cam(
                self.catalog.asset_banq1, cx1, cy1, zoom1, roll1, w, h
            )

            if trans_t < 1.0:
                frame_src = self.cam.render_doors_and_curtains(
                    self.catalog.pano, self.catalog, 80.0, 1.0, 0.0
                )
                cam_ext = self.cam.sample_virtual_cam(
                    frame_src,
                    (self.catalog.win_x1 + self.catalog.win_x2) / 2.0,
                    (self.catalog.win_y1 + self.catalog.win_y2) / 2.0,
                    3.45 + trans_t * 4.0,
                    roll1,
                    w,
                    h,
                )
                return (
                    cam_ext.astype(np.float32) * (1.0 - trans_t)
                    + cam1.astype(np.float32) * trans_t
                ).astype(np.uint8)
            return cam1

        # Phase 4: [330 to 430] FPV banking turn left into ballroom (banq2)
        elif f <= 430:
            t = (f - 330) / 100.0
            st = self.cam.smoothstep(t)
            bank_roll = -math.sin(st * math.pi) * 5.0

            b2_w, b2_h = self.catalog.asset_banq2.shape[1], self.catalog.asset_banq2.shape[0]
            turn_t = self.cam.ease_in_out(t)
            cx2 = (b2_w * 0.58) - turn_t * (b2_w * 0.16)
            cy2 = b2_h * 0.50
            zoom2 = 1.02 + turn_t * 0.25

            cam2 = self.cam.sample_virtual_cam(
                self.catalog.asset_banq2, cx2, cy2, zoom2, bank_roll, w, h
            )

            if t < 0.22:
                exit_t = t / 0.22
                b1_w, b1_h = self.catalog.asset_banq1.shape[1], self.catalog.asset_banq1.shape[0]
                cam1_exit = self.cam.sample_virtual_cam(
                    self.catalog.asset_banq1,
                    (b1_w / 2.0) + 120.0 + exit_t * 180.0,
                    b1_h / 2.0,
                    1.47,
                    bank_roll,
                    w,
                    h,
                )
                return (
                    cam1_exit.astype(np.float32) * (1.0 - exit_t)
                    + cam2.astype(np.float32) * exit_t
                ).astype(np.uint8)
            return cam2

        # Phase 5: [430 to 520] High-speed push down center aisle (banq3)
        elif f <= 520:
            t = (f - 430) / 90.0
            st = self.cam.ease_in_out(t)
            drone_roll = math.sin(t * math.pi) * 0.4

            b3_w, b3_h = self.catalog.asset_banq3.shape[1], self.catalog.asset_banq3.shape[0]
            cx3 = b3_w / 2.0
            cy3 = (b3_h * 0.58) - st * (b3_h * 0.12)
            zoom3 = 1.0 + st * 0.65

            cam3 = self.cam.sample_virtual_cam(
                self.catalog.asset_banq3, cx3, cy3, zoom3, drone_roll, w, h
            )

            if t < 0.16:
                trans_t = t / 0.16
                b2_w, b2_h = self.catalog.asset_banq2.shape[1], self.catalog.asset_banq2.shape[0]
                cam2_exit = self.cam.sample_virtual_cam(
                    self.catalog.asset_banq2,
                    b2_w * 0.42,
                    b2_h * 0.50,
                    1.27 + trans_t * 0.25,
                    drone_roll,
                    w,
                    h,
                )
                return (
                    cam2_exit.astype(np.float32) * (1.0 - trans_t)
                    + cam3.astype(np.float32) * trans_t
                ).astype(np.uint8)
            return cam3

        # Phase 6: [520 to 600] Royal wedding mandap arrival & hover (banq4)
        else:
            t = (f - 520) / 80.0
            t_ease = 1.0 - math.pow(1.0 - t, 3.0)
            drone_roll = math.sin(t * math.pi * 0.5) * 0.25

            b4_w, b4_h = self.catalog.asset_banq4.shape[1], self.catalog.asset_banq4.shape[0]
            cx4 = b4_w / 2.0
            cy4 = (b4_h * 0.52) - t_ease * (b4_h * 0.04)
            zoom4 = 1.02 + t_ease * 0.22

            cam4 = self.cam.sample_virtual_cam(
                self.catalog.asset_banq4, cx4, cy4, zoom4, drone_roll, w, h
            )

            if t < 0.20:
                trans_t = t / 0.20
                b3_w, b3_h = self.catalog.asset_banq3.shape[1], self.catalog.asset_banq3.shape[0]
                cam3_exit = self.cam.sample_virtual_cam(
                    self.catalog.asset_banq3,
                    b3_w / 2.0,
                    b3_h * 0.46,
                    1.65 + trans_t * 0.2,
                    drone_roll,
                    w,
                    h,
                )
                return (
                    cam3_exit.astype(np.float32) * (1.0 - trans_t)
                    + cam4.astype(np.float32) * trans_t
                ).astype(np.uint8)
            return cam4

    def render_video(
        self,
        output_path: Optional[str] = None,
        start_frame: int = 0,
        end_frame: Optional[int] = None,
        callback: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        """Renders the drone flight directly to an MP4 video file."""
        out_path = output_path or self.config.video_output
        total = self.config.total_frames
        end_f = end_frame if end_frame is not None else total

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            out_path, fourcc, self.config.fps, (self.config.width, self.config.height)
        )

        try:
            for f in range(start_frame, end_f):
                frame = self.render_frame(f)
                out.write(frame)
                if callback:
                    callback(f, total)
                elif f % 50 == 0 or f == end_f - 1:
                    pct = (f / total) * 100.0
                    print(f"Rendered video frame {f}/{total} ({pct:.1f}%)")
        finally:
            out.release()

        return out_path

    def export_webp_frames(
        self,
        output_dir: Optional[str] = None,
        quality: Optional[int] = None,
        start_frame: int = 0,
        end_frame: Optional[int] = None,
        callback: Optional[Callable[[int, int], None]] = None,
    ) -> int:
        """Renders and exports individual WebP frames for scrollytelling."""
        out_dir = output_dir or self.config.frames_dir
        os.makedirs(out_dir, exist_ok=True)
        q = quality or self.config.webp_quality
        total = self.config.total_frames
        end_f = end_frame if end_frame is not None else total

        encode_params = [int(cv2.IMWRITE_WEBP_QUALITY), q]
        count = 0

        for f in range(start_frame, end_f):
            frame = self.render_frame(f)
            fname = os.path.join(out_dir, f"frame_{f:04d}.webp")
            cv2.imwrite(fname, frame, encode_params)
            count += 1
            if callback:
                callback(f, total)
            elif f % 50 == 0 or f == end_f - 1:
                pct = (f / total) * 100.0
                print(f"Exported WebP frame {f}/{total} ({pct:.1f}%) -> {fname}")

        return count


def main():
    parser = argparse.ArgumentParser(description="FPV Drone Resort Tour Rendering Pipeline")
    parser.add_argument("--video", action="store_true", help="Render full MP4 video")
    parser.add_argument("--frames", action="store_true", help="Export WebP frames")
    parser.add_argument("--all", action="store_true", help="Render both video and WebP frames")
    parser.add_argument("--test-frame", type=int, help="Render and save a single test frame")
    parser.add_argument("--quality", type=int, default=80, help="WebP quality factor (1-100)")
    parser.add_argument("--output-video", type=str, default="resort_drone_flight.mp4")
    parser.add_argument("--output-frames", type=str, default="frames_webp")
    args = parser.parse_args()

    config = TourConfig(
        video_output=args.output_video,
        frames_dir=args.output_frames,
        webp_quality=args.quality,
    )
    pipeline = TourPipeline(config)

    if args.test_frame is not None:
        idx = args.test_frame
        frame = pipeline.render_frame(idx)
        out_name = f"test_frame_{idx:04d}.jpg"
        cv2.imwrite(out_name, frame)
        print(f"Saved test frame {idx} to {out_name}")
        return

    if args.all or (not args.video and not args.frames):
        print("=== Rendering Video & WebP Frames via Deep TourPipeline ===")
        pipeline.render_video()
        pipeline.export_webp_frames()
    elif args.video:
        print("=== Rendering Video via Deep TourPipeline ===")
        pipeline.render_video()
    elif args.frames:
        print("=== Exporting WebP Frames via Deep TourPipeline ===")
        pipeline.export_webp_frames()


if __name__ == "__main__":
    main()
