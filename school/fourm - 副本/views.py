from django.shortcuts import render
from django.core.paginator import Paginator
from login.models import person
# Create your views here.




def single(request):
    return render(request,'single.html')



#参数pIndex表示：当前要显示的页码
def page_test(request,pIndex):
    #查询所有的地区信息
    list1 = person.objects.all()
    #将地区信息按一页10条进行分页
    p = Paginator(list1, 8)
    #如果当前没有传递页码信息，则认为是第一页，这样写是为了请求第一页时可以不写页码
    if pIndex == '':
        pIndex = '1'
    #通过url匹配的参数都是字符串类型，转换成int类型
    pIndex = int(pIndex)
    n_pIndex = (pIndex + 1)
    nn_pIndex = (pIndex + 2)
    l_pIndex = (pIndex - 1)
    ll_pIndex = (pIndex - 2)

    #获取第pIndex页的数据
    list2 = p.page(pIndex)
    #获取所有的页码信息
    plist = p.page_range


    #将当前页码、当前页的数据、页码信息传递到模板中
    return render(request, 'fourm.html', {'list': list2, 'plist': plist, 'pIndex': pIndex,'n_pIndex':n_pIndex,'nn_pIndex':nn_pIndex,'l_pIndex':l_pIndex,'ll_pIndex':ll_pIndex,})