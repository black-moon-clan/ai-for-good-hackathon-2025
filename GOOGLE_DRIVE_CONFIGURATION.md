# Configure Google Cloud Console for Google Drive & Google Sheets API

## **📌 Step 1: Create a Google Cloud Project**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project **dropdown (top left)** and select **"New Project"**.
3. Enter a **Project Name** (e.g., `"Google-Drive-Sheets-API"`).
4. Click **"Create"** and wait for the project to be initialized.

---

## **📌 Step 2: Enable APIs**
1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project.
3. Go to **"APIs & Services" > "Library"**.
4. Enable the following APIs:
   - **Google Drive API**
   - **Google Sheets API**
5. Click **"Enable"** for each API.

---

## **📌 Step 3: Create a Service Account**
1. Go to **"IAM & Admin" > "Service Accounts"**.
2. Click **"Create Service Account"**.
3. Enter a **Name** and **Description** (e.g., `"Google API Service Account"`).
4. Click **"Create and Continue"**.
5. Assign a **Role**:
   - For Google Drive & Sheets, select:
     - **Editor** (Full access)
     - Or, manually choose:
       - `roles/drive.file`
       - `roles/spreadsheets`
6. Click **"Continue"**, then **"Done"**.
7. Rename the file service_account.json and put it in directory backend/config

---

## **📌 Step 4: Generate Service Account Key (JSON)**
1. Open **"IAM & Admin" > "Service Accounts"**.
2. Click on the **service account name**.
3. Go to the **"Keys"** tab.
4. Click **"Add Key"** > **"Create New Key"**.
5. Select **"JSON"**, then click **"Create"**.
6. A **JSON file** will be downloaded—**keep this safe** (you will use it in Python).

---

## **📌 Step 5: Share Google Drive Files with the Service Account**
Since the service account acts as a separate user, you **must share Google Drive files** with it.

### **Share a Google Drive Folder/File**
1. Open [Google Drive](https://drive.google.com/).
2. Select the **folder or file** you want the service account to access.
3. Click **"Share"** (top-right).
4. Enter the **service account email** (found in the JSON key file).
5. Set **permissions** to **Editor**.
6. Click **"Done"**.