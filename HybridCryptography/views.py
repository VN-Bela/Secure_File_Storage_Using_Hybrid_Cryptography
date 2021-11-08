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
            decrypt.decrypter()  # decrypt divide file

        return redirect(reverse('HybridCryptography:upload'))


class uploadView(generic.ListView):
    template_name = "HybridCryptography/upload.html"

    def get(self, request):
        return render(request, self.template_name)


class downloadView(generic.TemplateView):
    template_name = "HybridCryptography/download.html"


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
