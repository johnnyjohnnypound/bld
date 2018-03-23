from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.


def index(request):
    
    if request.META['HTTP_USER_AGENT'].lower().find('micromessenger') != -1 :
        return HttpResponse(
                (
                    '<!DOCTYPE html>'
                    '<body>'
                        '<img alt="badwechat" src="/media/badwechat.jpg" width="100%">'
                        '<script language="javascript"> '
                            'alert("微信内置浏览器无法下载，如需下载App请先选择在浏览器中打开");'
                            'window.location.href="/score";'
                        '</script>'
                    '</body>'
                    '</html>'
                )
            )
    return HttpResponseRedirect('/score/')
