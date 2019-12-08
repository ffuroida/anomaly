from django.http import HttpResponse
from django.shortcuts import render
from anomalydetection.forms.views import MahalanobisCreateForm

#method view

# def index(request):
#     if request.method == "POST":
#         form = MahalanobisCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(request.FILES['nama'])
#     return render(request, 'base/mahalanobis/index.html', {'form':MahalanobisCreateForm})
    
def index(request):
    data = {}
    if "GET" == request.method:
        return render(request, "base/mahalanobis/index.html", data)
        # if not GET, then proceed with processing
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("base/mahalanobis/index.html"))
            #if file is too large, return message
            if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("base/mahalanobis/index.html"))
               file_data = csv_file.read().decode("utf-8")          

               lines = file_data.split("\n")
            #loop over the lines and save them in db. If error shows up , store as string and then display
            for line in lines:                                           
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["nrp"] = fields[1]
            try:
            form = EventsForm(data_dict)
            if form.is_valid():
            form.save()                                   
            else:
            logging.getLogger("error_logger").error(form.errors.as_json())                                                                                     
            except Exception as e:
            logging.getLogger("error_logger").error(repr(e))                              
            pass

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload CVS file. "+repr(e))

                    return HttpResponseRedirect(reverse("base/mahalanobis/index.html"))