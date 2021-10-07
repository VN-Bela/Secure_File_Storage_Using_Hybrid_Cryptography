from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from .models import Document
from .forms import DocumentForm
from .import divide
from .import encrypt
from .import decrypt



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
            decrypt.decrypter()    # decrypt divide file

        return redirect(reverse('HybridCryptography:upload'))


class uploadview(generic.ListView):
    template_name = "HybridCryptography/upload.html"

    def get(self, request):
        return render(request, self.template_name)
