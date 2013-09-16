#coding=utf-8
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from proftpd.ftpadmin.forms.account import SignupForm, LoginForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from proftpd.ftpadmin.lib.common import initlog
from datetime import datetime, timedelta
import md5, cStringIO
from  django.conf.global_settings import LANGUAGE_COOKIE_NAME
from proftpd.ftpadmin.settings import APP_IMAGES
from proftpd.ftpadmin.lib.view_common import check_existing, upload_image


def uploadify(request):
    return render_to_response('ftpadmin/uploadify.html', context_instance=RequestContext(request))


def signup(request):
    return HttpResponseRedirect(reverse('site_index'))
#    if request.method == 'POST':
#        form = SignupForm(data=request.POST)
#        if form.is_valid():
#            new_user = form.save()
#            return HttpResponseRedirect(reverse('account_login'))
#    else:
#        form = SignupForm()
#    return render_to_response('admin/signup.html',
#                               { 'form': form })


@never_cache
def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            checkcod_s = request.session.get('checkcode', '')
            checkcod_q = request.POST.get('checkcode', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if checkcod_s  == checkcod_q and user is not None and user.is_active :
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('site_index'))
            else:
                return HttpResponseRedirect(reverse('account_login'))
        else:
            form = LoginForm()
        return render_to_response('admin/login.html',
                                   { 'form': form })
    else:
        return HttpResponseRedirect(reverse('site_index'))


 

def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('site_index'))







def get_check_code_image(request, image= APP_IMAGES+'/checkcode.gif'):
    import Image, ImageDraw, ImageFont, random
    logger2 = initlog()
    logger2.info("start get checkcode ..")
    font_file =  APP_IMAGES+'/Arial.ttf'
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    mp = md5.new()
    mp_src = mp.update(str(datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:6]
    draw.text((10,10), rand_str[0], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((48,10), rand_str[1], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((85,10), rand_str[2], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((120,10), rand_str[3], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((150,10), rand_str[4], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((180,10), rand_str[5], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    del draw
    request.session['checkcode'] = rand_str
    buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    return HttpResponse(buf.getvalue(),'image/gif')


def set_language(request): 
    from django.utils.translation import check_for_language 

    next = request.REQUEST.get('next', None) 
    if not next: 
        next = request.META.get('HTTP_REFERER', None) 
    if not next: 
        next = '/' 
    response = HttpResponseRedirect(next) 
    if request.method == 'POST': 
        lang_code = request.POST.get('language', None) 
        if lang_code and check_for_language(lang_code): 
            if hasattr(request, 'session'): 
                request.session['django_language'] = lang_code 
            max_age =  60*60*24*365 
            expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT") 
            response.set_cookie(LANGUAGE_COOKIE_NAME, lang_code, max_age, expires) 
    return response