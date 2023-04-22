import gradio as gr
import modules

import os
from pathlib import Path

def make_video(
        input_dir, output_filename,
        frame_rate=12, input_format='%07d.png'):
    
    os.system(
        f"ffmpeg -r {frame_rate} "
        f' -i "{Path(input_dir) / input_format}" '
        f" -c:v libx264 "
        f" -qp 0 "
        f' "{output_filename}" '
    )

def gr_show(visible=True):
    return {"visible": visible, "__type__": "update"}

class Script(modules.scripts.Script):
    def title(self):
        return "Video Util"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        input_extract_mode = gr.Dropdown(
            label='mode',
            choices=['extract', 'combine'],
            value='extract'
        )        
        input_dir = gr.Textbox(
            label='input_directory',
            placeholder='A directory or a file'
        )
        input_skip_frame = gr.Textbox(
            label='frame',
            placeholder='60'
        )
        output_dir = gr.Textbox(label='output_directory')

        return [
            input_dir,
            output_dir,
            input_skip_frame,
            input_extract_mode
        ]

    def run(self, p,
            input_dir,
            output_dir,
            input_skip_frame,
            input_extract_mode):

        if not input_dir:
            raise ValueError('input_dir is empty')
        if not output_dir:
            raise ValueError('output_dir is empty')

        input_dir = Path(input_dir)
        assert input_dir.exists()

        if input_extract_mode == 'combine':
            if input_dir.is_file():
                print("[combine] input directory")
                return None
            
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
            output_video_name = "output.mp4"
            print("combine images output.mp4")
            make_video(
                input_dir=input_dir,
                output_filename=output_dir/output_video_name,
                frame_rate=input_skip_frame
            )
        
        else:
            if input_dir.is_dir():
                print("[extract] input file")
                return None

            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)

            if input_skip_frame:
                os.system(f'ffmpeg -i "{input_dir}" -vf fps={input_skip_frame} "{output_dir / "%07d.png"}" ')
            else: 
                os.system(f'ffmpeg -i "{input_dir}" "{output_dir / "%07d.png"}" ')
    

        print(f"finish~\n")

        return None