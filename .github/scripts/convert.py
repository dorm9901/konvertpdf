import requests
import os
import base64
from github import Github

# Configuration
GH_TOKEN = os.getenv('GITHUB_TOKEN')  # Автоматически предоставляется GitHub Actions
REPO_NAME = os.getenv('GITHUB_REPOSITORY')  # Имя текущего репозитория (ваш/pdf-converter)
ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')  # Номер issue передан из workflow
CONVERTAPI_SECRET = os.getenv('CONVERTAPI_SECRET')  # Ваш секретный ключ
CONVERTAPI_URL = f'https://v2.convertapi.com/convert/pdf/to/doc?Secret={CONVERTAPI_SECRET}'

def main():
    # Initialize GitHub API client
    g = Github(GH_TOKEN)
    repo = g.get_repo(REPO_NAME)
    issue = repo.get_issue(number=int(ISSUE_NUMBER))

    # Check if the issue has any attachments (PDF)
    attachments = [comment for comment in issue.get_comments() if comment.body.startswith('PDF attached')]
    
    if not attachments:
        issue.create_comment("❌ Ошибка: Не найден прикрепленный PDF-файл.")
        return

    # Get the latest PDF attachment
    pdf_comment = attachments[-1]
    # Here you would need to parse the comment to get the download URL
    # This is a complex part because GitHub API doesn't directly give attachment URLs easily

    # This is a SIMPLIFIED example. In practice, you need to use the GitHub API to download the attachment.
    # Let's assume we have a direct download URL for the PDF (this is the hard part)
    pdf_url = "URL_TO_PDF_FROM_COMMENT"  # You need to implement this logic

    # Download PDF
    response = requests.get(pdf_url)
    pdf_data = response.content

    # Convert using ConvertAPI
    files = {'File': ('document.pdf', pdf_data, 'application/pdf')}
    payload = {'StoreFile': 'true'}
    response = requests.post(CONVERTAPI_URL, files=files, data=payload)
    
    if response.status_code != 200:
        issue.create_comment(f"❌ Ошибка конвертации: {response.text}")
        return

    # Get result
    result = response.json()
    docx_url = result['Files'][0]['Url']
    
    # Download DOCX
    docx_response = requests.get(docx_url)
    docx_data = docx_response.content

    # Upload back to GitHub as comment attachment
    # encoded_content = base64.b64encode(docx_data).decode()
    # repo.create_issue_comment(ISSUE_NUMBER, "✅ Конвертация завершена!", attachments=[{
    #     'filename': 'converted.docx',
    #     'content': encoded_content,
    #     'encoding': 'base64'
    # }])

    # Since GitHub API doesn't easily allow file uploads in comments,
    # we'll just provide a download link
    issue.create_comment(f"✅ Конвертация завершена! Скачайте файл: [converted.docx]({docx_url})")

if __name__ == '__main__':
    main()
