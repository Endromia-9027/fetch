from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def fetch_video_data(url):
    try:
        # Send a request to the provided URL
        response = requests.get(url)
        if response.status_code != 200:
            app.logger.error(f"Failed to fetch the webpage. Status code: {response.status_code}")
            return {"error": "Failed to fetch the webpage"}
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find video elements and extract data
        videos = []
        video_divs = soup.find_all('div', class_='video')
        
        for video_div in video_divs:
            title = video_div.find('p', class_='title').text if video_div.find('p', class_='title') else 'N/A'
            channel_name = video_div.find('p', class_='channel-name').text if video_div.find('p', class_='channel-name') else 'N/A'
            info = video_div.find('p', class_='info').text if video_div.find('p', class_='info') else 'N/A'
            time = video_div.find('div', class_='time').text if video_div.find('div', class_='time') else 'N/A'

            videos.append({
                'title': title,
                'channel_name': channel_name,
                'info': info,
                'time': time
            })
        
        return videos
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return {"error": "An internal error occurred"}

@app.route('/', methods=['GET'])
def show_main_screen():
    return "Hi"

@app.route('/fetch_videos', methods=['GET'])
def fetch_videos():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    app.logger.info(f"Fetching video data from URL: {url}")
    video_data = fetch_video_data(url)
    return jsonify(video_data)

@app.route('/channel_name', methods=['GET'])
def fetch_channel_names():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    app.logger.info(f"Fetching video data from URL: {url}")
    video_data = fetch_video_data(url)
    channel_names = [content['channel_name'] for content in video_data if 'channel_name' in content]
    return jsonify(channel_names)

@app.route('/info', methods=['GET'])
def fetch_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    app.logger.info(f"Fetching video data from URL: {url}")
    video_data = fetch_video_data(url)
    channel_names = [content['info'] for content in video_data if 'info' in content]
    return jsonify(channel_names)

@app.route('/time', methods=['GET'])
def fetch_time():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400
    
    app.logger.info(f"Fetching video data from URL: {url}")
    video_data = fetch_video_data(url)
    channel_names = [content['time'] for content in video_data if 'time' in content]
    return jsonify(channel_names)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
