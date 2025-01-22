from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util

def convert_md(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == "POST":
        # Get the search query safely
        entry_search = request.POST.get('q', '').strip()
        if entry_search:  # Check if search query is not empty
            html_content = convert_md(entry_search)
            if html_content is not None:
                return render(request, "encyclopedia/entry.html", {
                    "title": entry_search,
                    "content": html_content
                })
            else:
                # Partial match logic for recommendations
                all_entries = util.list_entries()
                recommendations = [
                    entry for entry in all_entries if entry_search.lower() in entry.lower()
                ]
                return render(request, "encyclopedia/search.html", {
                    "recommendations": recommendations
                })
def new_page(request):
    if request.method =="GET":
        return render(request, "encyclopedia/newpage.html")     
    else :
        title=request.POST['title']
        content=request.POST['content']
        titleExist= util.get_entry(title)
        if titleExist is not None:
            return render(request,"encyclopedia/error.html", {
                "message":"entry  page already exist "
            }) 
        else:
            util.save_entry(title, content)
            html_content= convert_md(title)
            return render(request,"encyclopedia/entry.html", {
                "title": title,
                "content": html_content,               
            })
def edit(request):
    if request.method=="POST":
        title = request.POST['entry_title']
        content= util.get_entry(title) 
        return render(request ,"encyclopedia/edit.html" , {
            "title":title,
            "content":content
        })
def save_edit(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content =convert_md(title)
        return render(request,"encyclopedia/entry.html" , {
            "title":title,
            "content":html_content
        })

def rand(request):
    all_entries = util.list_entries()
    rand_entry = random.choice(all_entries)
    html_content = convert_md(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })