
def get_ip_addr(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    ipaddr = x_forwarded_for.split(',')[0] if x_forwarded_for else \
        request.META.get('REMOTE_ADDR')
    return ipaddr or None
