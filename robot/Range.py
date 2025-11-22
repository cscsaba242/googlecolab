
'''
This range class makes the ranges list based on 
start: timestamp
end: timestamp
interval: stock data time interval 1, 5, 15, 30, 60 (minutes) - should no bigger than end - start (diff)
(interval is in minute)
max per request: data provider max data points per request
'''
class Range():

  def rolling_pages(self, start, end, interval, max_per_request):
    # start must be less then end
    diff = end - start
    if diff < 0:
        raise Exception("end must be > start ")

    if diff < interval:
        print("warning: diff < interval, too early to the request")
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

  def calcPages(self, start: int, end: int, interval: int, max_per_request: int):
    self.pages = []
    self._gen_pages = self.rolling_pages(start, end, interval, max_per_request)
    pages = list(self._gen_pages)
    pages_count = len(pages)
    i = 0
    while i < pages_count - 1:
      self.pages.append([pages[i], pages[i+1]])
      i += 1
    self.len_pages = i

