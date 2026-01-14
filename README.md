📡 Computer Networks Final Project
TCP Chat Application & Network Traffic Analysis
ברוכים הבאים לרפוזיטורי של פרויקט גמר בקורס רשתות תקשורת מחשבים.
הפרויקט משלב בין ניתוח תעבורת רשת לבין פיתוח יישום תקשורת מבוסס TCP, ומחולק לשני חלקים מרכזיים.
________________


📚 Part 1 - Network Traffic Simulation & Wireshark Analysis
קבצים רלוונטיים:
* raw_tcp_ip_notebook_fallback_annotated-v1.ipynb
* group212055024.xls
* PartOneNetworking.pcap
בחלק זה בוצעה סימולציה של תהליך Encapsulation של מידע ברשת, החל משכבת האפליקציה ועד שכבת הרשת.
מה בוצע בחלק זה:
* יצירת קובץ נתונים (CSV) באופן ידני המדמה הודעות בשכבת האפליקציה.
* עיבוד הנתונים באמצעות Jupyter Notebook.
* הדמיית אריזת המידע בפרוטוקולי TCP/IP.
* לכידת התעבורה באמצעות Wireshark.
* ניתוח החבילות והבנת מבנה המידע המועבר ברשת.
ניתוח מפורט של המנות והפרוטוקולים מופיע בדוח המסכם.
________________


💬 Part 2 – TCP Chat Application
קבצים רלוונטיים:
* server.py
* client.py
* PartTwoNetworking.pcap
📌 תיאור כללי
בחלק זה פותחה אפליקציית צ’אט הפועלת בארכיטקטורת Client - Server מעל פרוטוקול TCP.
המערכת מאפשרת תקשורת בזמן אמת בין מספר משתמשים מקומיים.
🔧 מאפייני המערכת
* שרת מרכזי המנהל חיבורים של לקוחות.
* תמיכה במספר משתמשים בו זמנית.
* ניהול רשימת משתמשים מחוברים.
* שליחת הודעות פרטיות בין משתמשים.
* שימוש ב- Multi-threading למניעת קיפאון בממשק.
🎨 ממשק משתמש 
* מימוש באמצעות tkinter.
* בועות הודעה לשיחות נכנסות ויוצאות.
* הצגת הודעות מערכת (כגון ניתוק משתמש).
________________


🛠️ דרישות מערכת (Prerequisites)
חובה:
* Python 3.x (מומלץ 3.6 ומעלה)
ספריות נדרשות:
הפרויקט משתמש אך ורק בספריות מובנות של Python:
* socket
* threading
* tkinter
❗ אין צורך לבצע pip install


⚠️ בעיות נפוצות – tkinter
שגיאה:
ModuleNotFoundError: No module named 'tkinter'


פתרון לפי מערכת הפעלה
🪟 Windows
1. פתחי Settings → Apps → Python
2. לחצי Modify
3. ודאי שהאפשרות tcl/tk and IDLE מסומנת ✔️
4. המשיכי בהתקנה
🍎 macOS
brew install python-tk


בדיקה שהכל תקין
python -m tkinter
אם נפתח חלון קטן - tkinter מותקן בהצלחה.


🚀 How to Run the Project
⚠️ חשוב: יש להפעיל קודם את השרת ורק לאחר מכן את הלקוחות.
שלב 1 – הפעלת השרת
python server.py
פלט צפוי:
Server is Up and listening
⚠️ אין לסגור את חלון השרת בזמן העבודה.








שלב 2 – הפעלת לקוח (GUI)
בחלון Terminal חדש:
python client.py


* הזינו שם משתמש ייחודי
* לחצו על Connect
* בחרו משתמש מהרשימה והתחילו לשוחח
פתיחת משתמשים נוספים
פשוט פתחו Terminal נוסף והריצו שוב:
python client.py


________________


📡 Network Traffic Analysis
במהלך השימוש באפליקציה בוצעה לכידת תעבורה ב־Wireshark, הכוללת:
* TCP Three-Way Handshake
* שליחת הודעות
* חבילות ACK
* אירועי ניתוק (FIN)
________________


👥 Authors
* עדן זרביאן
* נטע גולזאד
