from django.shortcuts import render, redirect

# Create your views here.
from app.models import *


def book(request):
    publishs = Publish.objects.all()
    books = Book.objects.all()
    authors = Author.objects.all()

    context = {
        'publishs': publishs,
        'books': books,
        'authors': authors
    }
    return render(request, 'book.html', context)


def delbook(request, id):
    book = Book.objects.filter(id=id).first()

    authors = book.author.all()
    for author in authors:
        if author.book_set.count() == 1:
            author.delete()
    if book.category.book_set.count() <= 1:
        book.category.delete()
    if book.publish.book_set.count() <= 1:
        book.publish.delete()
    book.delete()

    return redirect('/book/')


def addbook(request):
    if request.method == 'POST':
        publish = Publish.objects.get_or_create(name=request.POST.get('publish'))[0]
        category = Category.objects.get_or_create(name=request.POST.get('category'))[0]
        book = Book.objects.create(name=request.POST.get('book'), publish=publish, category=category)
        authors = request.POST.get('authors').split()
        for author in authors:
            i = Author.objects.get_or_create(name=author)[0]
            book.author.add(i)

        return redirect('/book/')

    return render(request, 'addbook.html')


def searchbook(request):
    if request.method == 'GET':
        return redirect('/book/')

    if request.method == 'POST':
        value = request.POST.get('value')
        type = request.POST.get('type')

        if type == 'book':
            books = Book.objects.filter(name__contains=value)
        if type == 'publish':
            books = Publish.objects.get(name__contains=value).book_set.all()
        if type == 'author':
            books = Author.objects.get(name__contains=value).book_set.all()

    return render(request, 'searchbook.html', {'books': books})


def editbook(request, id):
    books = Book.objects.filter(id=id)
    book = books.first()
    authors = book.author.all().order_by('name')
    comments = book.comment_set.all()
    context = {
        'book': book,
        'authors': authors,
        'comments': comments,
    }
    if request.method == 'POST' or request.method == 'FILES':
        b_name = request.POST.get('book')
        p_name = request.POST.get('publish')
        p_tel = request.POST.get('p_tel')
        p_city = request.POST.get('p_city')
        p_email = request.POST.get('p_email')
        p_description = request.POST.get('p_description')
        c_name = request.POST.get('category')

        book.name = b_name
        book.save()
        publish = \
            Publish.objects.get_or_create(name=p_name, city=p_city, tel=p_tel, email=p_email,
                                          description=p_description)[0]
        category = Category.objects.get_or_create(name=c_name)[0]
        books.update(name=b_name, publish=publish, category=category)
        for i in Publish.objects.all():
            if not i.book_set.all():
                i.delete()
        # 多对多修改
        names = request.POST.getlist('a_name')
        descriptions = request.POST.getlist('a_description')
        ages = request.POST.getlist('a_age')
        countrys = request.POST.getlist('a_country')
        postcodes = request.POST.getlist('a_postcode')

        set_list = []
        for name, description, age, country, postcode in zip(names, descriptions, ages, countrys, postcodes):
            obj = Author.objects.get_or_create(name=name, description=description, age=age, country=country,
                                               postcode=postcode)[0]
            set_list.append(obj.id)
        book.author.set(set_list)
        for i in Author.objects.all():
            if not i.book_set.all():
                i.delete()

        return redirect('/book/')
    return render(request, 'editbook.html', context)


def details(request, id):
    book = Book.objects.get(id=id)
    authors = book.author.all()
    comments = book.comment_set.all()
    context = {
        'book': book,
        'authors': authors,
        'comments': comments
    }
    return render(request, 'test.html', context)
