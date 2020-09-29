
def sendmail(request):
    template="contact.html"

    df_file = pd.read_csv("/Users/ashishkumar/Desktop/email.csv")
    df=pd.DataFrame(df_file)

    list = df['Email'].tolist()

    if request.method=="POST" and  request.FILES['file']:
        
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email=settings.EMAIL_HOST_USER
        file = request.FILES['file']
        file_name = default_storage.save(file.name, file)
        connection = mail.get_connection()
        connection.open()
        

        email= mail.EmailMessage(subject, message, from_email,bcc=list,connection=connection )

        file = default_storage.open(file_name)
        file_url = default_storage.url(file_name)
        email.attach(file_url, file.read())
        connection.send_messages([email])

        print(list)


        messages.success(request,"Email sent Successfully")
  
        connection.close()
    
    return render(request,'contact.html')

