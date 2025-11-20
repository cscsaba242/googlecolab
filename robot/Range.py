
# ....T....T.....P....T....T.....P
# This range class will do the ranges list based on start, end, interval and max per request 
# The smallest interval is a minute
class Range():

    
  def rolling_pages(self, start, end, interval, max_per_request):
    # start must be less then end
    diff = end - start
    if diff < 0:
        raise Exception("end must be > start ")

    if diff < interval:
        print("diff < interval, too early to the request")
        return

    page = max_per_request * interval

    if page > diff:
        page = diff

    remainder = diff % page
            
    for result in range(start, end, page):
            yield result          
    if remainder > 0:
        yield result + remainder
    else:
        yield end
