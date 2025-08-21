import os
import cv2
from PIL import Image
import numpy as np
import psutil
import gc
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import threading
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


class MP4ToWebPConverter:
    def __init__(self):
        self.conversion_status = {
            'is_converting': False,
            'progress': 0,
            'current_file': '',
            'total_files': 0,
            'completed_files': 0,
            'message': ''
        }
        self.current_output_folder = app.config['OUTPUT_FOLDER']

    def set_output_folder(self, folder_path):
        """출력 폴더 설정"""
        # 절대 경로로 변환
        folder_path = os.path.abspath(folder_path)

        # 폴더가 존재하지 않으면 생성 시도
        try:
            os.makedirs(folder_path, exist_ok=True)
        except Exception as e:
            return False, f"폴더 생성 실패: {str(e)}"

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            self.current_output_folder = folder_path
            return True, "성공"

        return False, "유효하지 않은 폴더입니다"

    def get_available_drives(self):
        """사용 가능한 드라이브 목록 반환 (Windows)"""
        drives = []
        if os.name == 'nt':  # Windows
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    try:
                        # 드라이브 정보 가져오기
                        total, used, free = psutil.disk_usage(drive)
                        drives.append({
                            'letter': letter,
                            'path': drive,
                            'name': f"{letter}: 드라이브",
                            'free_space': self.format_bytes(free),
                            'total_space': self.format_bytes(total)
                        })
                    except:
                        drives.append({
                            'letter': letter,
                            'path': drive,
                            'name': f"{letter}: 드라이브",
                            'free_space': 'Unknown',
                            'total_space': 'Unknown'
                        })
        else:  # Unix/Linux/Mac
            drives.append({
                'letter': '/',
                'path': '/',
                'name': '루트 디렉토리',
                'free_space': 'N/A',
                'total_space': 'N/A'
            })
        return drives

    def format_bytes(self, bytes_value):
        """바이트를 읽기 쉬운 형태로 변환"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def list_directory(self, path):
        """디렉토리 내용 나열"""
        try:
            items = []

            # 상위 디렉토리 추가 (루트가 아닌 경우)
            parent = os.path.dirname(path)
            if parent != path:  # 루트 디렉토리가 아닌 경우
                items.append({
                    'name': '..',
                    'path': parent,
                    'type': 'parent',
                    'size': 0
                })

            # 현재 디렉토리의 폴더들만 나열
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    try:
                        # 숨김 폴더 제외 (Windows)
                        if os.name == 'nt' and item.startswith('.'):
                            continue

                        items.append({
                            'name': item,
                            'path': item_path,
                            'type': 'folder',
                            'size': 0
                        })
                    except PermissionError:
                        # 접근 권한이 없는 폴더는 건너뛰기
                        continue

            return items
        except Exception as e:
            return []

    def get_optimal_batch_size(self):
        """시스템 메모리에 따른 최적 배치 크기 계산"""
        available_memory = psutil.virtual_memory().available
        memory_gb = available_memory / (1024 ** 3)

        if memory_gb >= 16:
            return 1000
        elif memory_gb >= 8:
            return 500
        elif memory_gb >= 4:
            return 250
        else:
            return 100

    def convert_files(self, file_paths, settings):
        """파일 변환 (백그라운드 스레드에서 실행)"""
        self.conversion_status['is_converting'] = True
        self.conversion_status['total_files'] = len(file_paths)
        self.conversion_status['completed_files'] = 0

        try:
            for i, file_path in enumerate(file_paths):
                filename = os.path.basename(file_path)
                self.conversion_status['current_file'] = filename
                self.conversion_status['message'] = f'변환 중: {filename}'

                self.convert_single_file(file_path, settings)

                self.conversion_status['completed_files'] += 1
                self.conversion_status['progress'] = int((i + 1) / len(file_paths) * 100)

            self.conversion_status['message'] = f'모든 파일 변환 완료! 저장 위치: {self.current_output_folder}'

        except Exception as e:
            self.conversion_status['message'] = f'오류: {str(e)}'
        finally:
            self.conversion_status['is_converting'] = False

    def convert_single_file(self, file_path, settings):
        """단일 파일 변환"""
        cap = None
        try:
            cap = cv2.VideoCapture(file_path)

            if not cap.isOpened():
                raise Exception(f"비디오 파일을 열 수 없습니다: {file_path}")

            # 원본 비디오 정보
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / original_fps if original_fps > 0 else 0

            if total_frames <= 0 or original_fps <= 0:
                raise Exception("유효하지 않은 비디오 파일입니다")

            # 설정 적용
            target_fps = settings['fps']
            frame_interval = max(1, int(original_fps / target_fps)) if original_fps > 0 else 1

            # 안전한 파일명 생성
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            safe_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_name:
                safe_name = "converted"

            output_filename = f"{safe_name}.webp"
            output_path = os.path.join(self.current_output_folder, output_filename)

            # 파일이 이미 존재하면 번호 추가
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{safe_name}_{counter}.webp"
                output_path = os.path.join(self.current_output_folder, output_filename)
                counter += 1

            # 프레임 수집
            frames = []
            frame_count = 0

            for current_frame in range(total_frames):
                if current_frame % frame_interval != 0:
                    continue

                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                ret, frame = cap.read()

                if not ret:
                    continue

                # 크기 조정
                if settings['size_type'] and settings['pixel_size']:
                    frame = self.resize_frame(frame, settings)

                # BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                frames.append(pil_image)

                frame_count += 1

                # 메모리 체크
                if frame_count % 200 == 0:
                    memory_percent = psutil.virtual_memory().percent
                    if memory_percent > 85:
                        gc.collect()

            cap.release()
            cap = None

            if not frames:
                raise Exception("추출된 프레임이 없습니다")

            # 프레임 지속 시간
            frame_duration = int(1000 / target_fps)

            # 품질 설정
            if settings['lossless']:
                effective_quality = 100
            else:
                compression_factor = settings['compression'] / 100
                effective_quality = int(settings['quality'] * (1 - compression_factor * 0.5))
                effective_quality = max(10, min(100, effective_quality))

            # WebP 저장
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=frame_duration,
                loop=0,
                lossless=settings['lossless'],
                quality=effective_quality,
                method=0,
                optimize=False
            )

            # 메모리 정리
            frames = []
            gc.collect()

        except Exception as e:
            if cap is not None:
                cap.release()
            gc.collect()
            raise e

    def resize_frame(self, frame, settings):
        """프레임 크기 조정"""
        h, w = frame.shape[:2]

        if settings['size_type'] == 'width':
            new_w = settings['pixel_size']
            new_h = int(h * (settings['pixel_size'] / w))
        else:  # height
            new_h = settings['pixel_size']
            new_w = int(w * (settings['pixel_size'] / h))

        return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)


# 전역 변환기 인스턴스
converter = MP4ToWebPConverter()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """파일 업로드 처리"""
    try:
        files = request.files.getlist('files')
        uploaded_files = []

        for file in files:
            if file and file.filename.lower().endswith('.mp4'):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                unique_filename = timestamp + filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                uploaded_files.append({
                    'name': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path)
                })

        return jsonify({'success': True, 'files': uploaded_files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/browse_folders')
def browse_folders():
    """웹 기반 폴더 브라우저"""
    path = request.args.get('path', '')

    if not path:
        # 시작 경로: 사용 가능한 드라이브 목록
        drives = converter.get_available_drives()
        return jsonify({
            'success': True,
            'current_path': '',
            'items': drives,
            'type': 'drives'
        })

    try:
        items = converter.list_directory(path)
        return jsonify({
            'success': True,
            'current_path': path,
            'items': items,
            'type': 'folders'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/set_output_folder', methods=['POST'])
def set_output_folder():
    """출력 폴더 설정"""
    try:
        data = request.get_json()
        folder_path = data.get('folder_path', '').strip()

        if not folder_path:
            return jsonify({'success': False, 'error': '폴더 경로를 입력해주세요'})

        success, message = converter.set_output_folder(folder_path)

        if success:
            return jsonify({
                'success': True,
                'folder': converter.current_output_folder,
                'message': f'출력 폴더가 설정되었습니다: {converter.current_output_folder}'
            })
        else:
            return jsonify({'success': False, 'error': message})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_output_folder')
def get_output_folder():
    """현재 출력 폴더 조회"""
    return jsonify({'folder': converter.current_output_folder})


@app.route('/convert', methods=['POST'])
def start_conversion():
    """변환 시작"""
    try:
        data = request.get_json()
        file_paths = data['file_paths']
        settings = data['settings']

        # 백그라운드에서 변환 실행
        thread = threading.Thread(target=converter.convert_files, args=(file_paths, settings))
        thread.daemon = True
        thread.start()

        return jsonify({'success': True, 'message': '변환이 시작되었습니다'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/status')
def get_status():
    """변환 상태 조회"""
    return jsonify(converter.conversion_status)


@app.route('/download/<filename>')
def download_file(filename):
    """변환된 파일 다운로드"""
    try:
        file_path = os.path.join(converter.current_output_folder, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/outputs')
def list_outputs():
    """변환된 파일 목록"""
    try:
        output_files = []
        if os.path.exists(converter.current_output_folder):
            for filename in os.listdir(converter.current_output_folder):
                if filename.endswith('.webp'):
                    file_path = os.path.join(converter.current_output_folder, filename)
                    output_files.append({
                        'name': filename,
                        'size': os.path.getsize(file_path),
                        'modified': os.path.getmtime(file_path)
                    })
        return jsonify(output_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/open_output_folder')
def open_output_folder():
    """출력 폴더 열기"""
    try:
        import subprocess
        import platform

        folder_path = converter.current_output_folder

        if platform.system() == 'Windows':
            subprocess.run(['explorer', folder_path])
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', folder_path])
        else:  # Linux
            subprocess.run(['xdg-open', folder_path])

        return jsonify({'success': True, 'message': f'폴더를 열었습니다: {folder_path}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    """서버 종료"""
    try:
        import os
        import signal
        import threading

        def shutdown():
            # 1초 후 서버 종료
            import time
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)

        # 백그라운드에서 종료 실행
        thread = threading.Thread(target=shutdown)
        thread.daemon = True
        thread.start()

        return jsonify({'success': True, 'message': '서버가 종료됩니다.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    print("🎬 MP4 to WebP 변환기 웹 서버 시작")
    print("폴더에서 GUI를 실행하거나, 브라우저에서 http://localhost:5000 으로 접속하세요")
    app.run(debug=True, host='0.0.0.0', port=5000)