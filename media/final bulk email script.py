
def sendmail(request):
    template="contact.html"

    if request.method=="POST" and  request.FILES['file'] and request.FILES['csv_files']:
        
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email=settings.EMAIL_HOST_USER
        csv = request.FILES['csv_files']
        csv_file_name = default_storage.save(csv.name, csv)

        csv_file = default_storage.open(csv_file_name)
        csv_file_url = default_storage.url(csv_file_name)
        print(csv_file_url)
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        connection = mail.get_connection()
        connection.open()

        df_file = pd.read_csv(csv_file)
        print(df_file)

        df = pd.DataFrame(df_file)

        list = df['Email'].tolist()
        

        email= mail.EmailMessage(subject, message, from_email,bcc=list,connection=connection )

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])



        messages.success(request,"Email sent Successfully")
  
        connection.close()

    return render(request,'contact.html')

