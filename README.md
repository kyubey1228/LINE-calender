# LINE Bot スケジューラー

このプロジェクトは、LINE を通じて Google Calendar にイベントを追加するボットです。ユーザーが LINE でメッセージを送信すると、OpenAI GPT-3.5 を使用してメッセージを解析し、スケジュール情報を抽出して Google Calendar に追加します。

## 機能

- LINE メッセージからスケジュール情報を抽出
- 抽出した情報を Google Calendar に追加
- 追加結果を LINE で返信

## セットアップ

1. このリポジトリをクローンします。

2. 必要なパッケージをインストールします：

   ```
   pip install -r requirements.txt
   ```

3. `config.py`ファイルを作成し、以下の情報を設定します：

   - LINE Channel Access Token
   - LINE Channel Secret
   - Google Calendar API の認証情報
   - OpenAI API Key

4. Google Cloud Console で新しいプロジェクトを作成し、Google Calendar API を有効にします。サービスアカウントを作成し、JSON キーをダウンロードします。

5. LINE デベロッパーコンソールで新しいチャネルを作成し、必要な情報を取得します。

6. OpenAI API キーを取得します。

## 使用方法

1. アプリケーションを起動します：

   ```
   python app.py
   ```

2. ngrok などのツールを使用して、ローカルサーバーを公開 URL にフォワーディングします。

3. LINE デベロッパーコンソールで、Webhook URL を設定します（例：`https://your-domain.ngrok.io/callback`）。

4. LINE アプリでボットを友達追加し、スケジュール情報をメッセージとして送信します（例：「明日 15 時から会議」）。

5. ボットがメッセージを解析し、Google Calendar にイベントを追加した後、結果を LINE で返信します。

## 注意事項

- `config.py`ファイルには機密情報が含まれるため、Git リポジトリにコミットしないよう注意してください。
- このアプリケーションは開発環境での使用を想定しています。本番環境で使用する場合は、セキュリティ対策を十分に行ってください。
