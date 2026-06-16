from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

API_URL = 'https://ws-okdkdsbtqwyb5im6.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions'
API_KEY = 'sk-ws-H.REMXPEY.xzZe.MEUCIC3yjMytpicJxRFoyn9AbdTU0KN6Z_NAW2QBC10GGTDFAiEAiMjxCgMOVAzhPCgVLs3AkdQfKVcQBUqY8APFBWKzY08'

@app.route('/')
def index():
    return send_file('低情商转高情商.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_text = data.get('input', '').strip()
        tone = data.get('tone', 'warm')
        
        if not input_text:
            return jsonify({'success': False, 'error': '请输入要转换的话术'})
        
        tone_prompt = {
            'warm': '温暖体贴、善解人意的表达方式',
            'professional': '专业、得体、正式的表达方式',
            'humorous': '幽默、风趣、轻松的表达方式',
            'encouraging': '鼓励、激励、积极向上的表达方式'
        }.get(tone, '温暖体贴的表达方式')
        
        response = requests.post(
            API_URL,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json={
                'model': 'qwen3.6-flash',
                'messages': [{
                    'role': 'user',
                    'content': f'请将这句低情商的话改写成{tone_prompt}（只说改写结果，不要解释）："{input_text}"'
                }],
                'temperature': 0.7
            }
        )
        
        if not response.ok:
            error_data = response.json()
            return jsonify({'success': False, 'error': error_data.get('error', {}).get('message', 'API调用失败')})
        
        result = response.json()
        output_text = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        if not output_text:
            return jsonify({'success': False, 'error': '未获取到转换结果'})
        
        return jsonify({'success': True, 'output': output_text})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🎨 低情商转高情商工具启动成功！")
    print("🌐 访问地址: http://localhost:5000")
    print("🔗 保持此窗口打开，关闭后工具将停止运行")
    print("💡 提示：可以把这个链接分享给同一网络内的朋友")
    app.run(host='0.0.0.0', port=5000, debug=False)