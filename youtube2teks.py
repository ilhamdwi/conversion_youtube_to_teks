import os
import speech_recognition as sr
from pytube import YouTube
from moviepy.editor import VideoFileClip

def download_youtube_video(url, output_path="."):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        
        print(f"Downloading: {yt.title}")
        video_stream.download(output_path)
        print("Download completed!")
        
        return yt.title
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_video_to_audio(video_file, audio_output_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_output_file)

def clean_filename(filename):
    forbidden_chars = r'<>:"/\|?*'  # Karakter yang tidak diizinkan dalam nama file
    cleaned_filename = "".join([char for char in filename if char not in forbidden_chars])
    return cleaned_filename

def convert_audio_to_text(audio_file, lang):
    r = sr.Recognizer()
    all_text = []

    with sr.AudioFile(audio_file) as source:
        print("Fetching audio...")
        audio_text = r.listen(source)
        try:
            print("Converting audio to text...")
            text = r.recognize_google(audio_text, language=lang)
            all_text.append(text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return all_text

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=-6g9LL7JWAA"
    output_path = "downloaded_videos"
    lang = "id"

    video_title = download_youtube_video(video_url, output_path)
    if video_title:
        cleaned_video_title = clean_filename(video_title)
        video_file = f"{output_path}/{cleaned_video_title}.mp4"
        audio_file = f"{output_path}/{cleaned_video_title}.wav"

        print("Video downloaded, now converting to audio...")
        convert_video_to_audio(video_file, audio_file)

        print("Audio conversion completed, now converting to text...")
        text_result = convert_audio_to_text(audio_file, lang)

        if text_result:
            output_text_file = f"file_text/{cleaned_video_title}.txt"
            with open(output_text_file, "w") as txt_file:
                txt_file.write("\n".join(text_result))
            
            print(f"Converted text saved to {output_text_file}")
        else:
            print("No text to save.")
