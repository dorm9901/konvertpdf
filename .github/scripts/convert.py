import os
import requests
from github import Github

def main():
    try:
        # Получаем секреты и данные из переменных окружения GitHub Actions
        github_token = os.environ['GITHUB_TOKEN']
        convertapi_secret = os.environ['CONVERTAPI_SECRET']
        repo_name = os.environ['GITHUB_REPOSITORY']
        issue_number = int(os.environ['ISSUE_NUMBER'])

        print(f"🚀 Starting conversion for issue #{issue_number}")

        # Создаем клиент для работы с GitHub API
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)

        # Оставляем комментарий о начале конвертации
        issue.create_comment("🔄 Запускаю конвертацию PDF в Word...")

        # Проверяем, есть ли метка convert
        labels = [label.name for label in issue.labels]
        if 'convert' not in labels:
            error_msg = "❌ Issue doesn't have 'convert' label. Please add the 'convert' label to this issue."
            issue.create_comment(error_msg)
            print(error_msg)
            return

        # Ищем комментарии с вложениями (это сложная часть с GitHub API)
        comments = issue.get_comments()
        pdf_found = False

        for comment in comments:
            if 'PDF file attached' in comment.body:
                pdf_found = True
                # Здесь должен быть код для обработки вложения
                break

        if not pdf_found:
            issue.create_comment("❌ No PDF file found. Please attach a PDF file to the issue comments.")
            print("No PDF file found in comments")
            return

        # ЗДЕСЬ БУДЕТ КОД ДЛЯ РАБОТЫ С ConvertAPI
        # Это временная заглушка для теста
        print("✅ Conversion simulation completed successfully")
        issue.create_comment("✅ Конвертация успешно завершена! (Это тестовое сообщение)\n\n"
                           "⚠️ Реальная конвертация через ConvertAPI будет реализована в следующем шаге.")

    except Exception as e:
        error_msg = f"❌ Critical error: {str(e)}"
        print(error_msg)
        # Пытаемся добавить комментарий об ошибке в issue
        try:
            issue.create_comment(error_msg)
        except:
            pass

if __name__ == '__main__':
    main()
