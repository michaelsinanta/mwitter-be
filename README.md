Nama : Michael Christlambert Sinanta<br>
Stack : Django Rest Framework<br>

Cara instalasi sesudah mengclone github ini adalah sebagai berikut: 
1. python3 -m pip install -r requirements.txt
2. python3 manage.py makemigrations
3. python3 manage.py migrate
4. python3 manage.py runserver 

Untuk mengakses administrator page pada django, pengguna dapat menggunakan admin yang sudah dibuat dengan keterangan sebagai berikut :
1. email : m@example.com
2. password : javascript

Jika pengguna ingin membuat admin sendiri, maka dapat menjalankan perintah pada terminal sebagai berikut :
1. python3 manage.py createsuperuser
Kemudian, isi data pada terminal.<br>

Setelah admin terbuat, pengguna dapat mengakses pada link http://localhost:8000/admin.<br>

Sesudah backend dijalankan, jalankan frontendnya juga. Backend dapat diakses melalui link http://localhost:8000/.