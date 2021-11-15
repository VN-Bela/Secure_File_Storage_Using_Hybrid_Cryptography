from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from .models import Document
from .forms import DocumentForm
from . import divide
from . import encrypt
from . import decrypt
from . import combine
from . import tools
import mimetypes
from django.http.response import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


# Create your views here.

class IndexView(generic.CreateView):
    model = Document
    template_name = "HybridCryptography/index.html"
    form_class = DocumentForm

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST or None, request.FILES)
        if form.is_valid():
            # DocForm = form.save(commit=False)
            form.save()
            fname = request.FILES['filename'].name
            divide.divider(fname)  # divide function call (to divide file)
            encrypt.encrypter()  # encrypt divided file
        # decrypt.decrypter()  # decrypt divide file

        return redirect(reverse('HybridCryptography:upload'))


class uploadView(generic.ListView):
    template_name = "HybridCryptography/upload.html"

    def get(self, request):
        return render(request, self.template_name)


class KeyUploadView(generic.CreateView):
    model = Document
    template_name = "HybridCryptography/Key_Upload.html"
    form_class = DocumentForm

    #def get(self, request):
        #return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = DocumentForm(request.POST or None, request.FILES)
        if form.is_valid():
            # DocForm = form.save(commit=False)
            form.save()
            fname = request.FILES['filename'].name
            print(fname)
            decrypt.decrypter(fname)
        return render(request, "HybridCryptography/upload.html")


class downloadView(generic.TemplateView):
    template_name = "HybridCryptography/File_download.html"

    def get(self, request):
        return render(request, self.template_name)


def download_file(request):
    print("Before call merge")
    combine.merge()
    print("After call merge")
    list_dir = tools.list_dir('restore')
    file_name = 'restore/' + list_dir[0]
    path = open(file_name, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(file_name)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    # Return the response value
    return response


class successView(generic.TemplateView):
    template_name = "HybridCryptography/success.html"

    def get(self, request):
        return render(request, self.template_name)


def email_send(recipient):
    # send_mail(subject='Demo Subject', message='Demo Message', from_email=settings.EMAIL_HOST_USER,
    print(recipient)
    msg = EmailMessage(subject='Demo Subject', body='Demo Message', from_email=settings.EMAIL_HOST_USER,
                       to=[recipient])
    msg.attach_file('Key/private.pem')
    msg.send()


class KeySendView(generic.ListView):
    template_name = "HybridCryptography/Key_Send.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("recipient_email")
        print(email)
        email_send(email)
        return render(request, "HybridCryptography/Email_send.html")
