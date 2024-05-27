import base64

def encode_pdf_to_base64(pdf_file_path):
    # PDF ファイルをバイナリモードで開きます
    with open(pdf_file_path, 'rb') as pdf_file:
        # PDF ファイルの内容を読み取ります
        pdf_content = pdf_file.read()
        
        # 読み取った PDF ファイルの内容を Base64 エンコードします
        encoded_pdf = base64.b64encode(pdf_content)
        
        return encoded_pdf.decode('utf-8')  # Base64 エンコードされたデータを文字列として返します

# PDF ファイルのパス
pdf_file_path = '/home/soft/github/world-wing/aska-backend/sandbox/nakayama/お座りお馬さん.pdf'

# PDF ファイルを Base64 エンコードします
base64_encoded_pdf = encode_pdf_to_base64(pdf_file_path)

# エンコードされたデータを表示します
print(base64_encoded_pdf)
