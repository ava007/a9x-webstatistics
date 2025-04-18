# -*- coding: utf-8 -*-
from operator import itemgetter

def qualitystatus500(d, owndomain, omit):

    # status codes 500 for max 30 days:
    h = ''
    tquality = {}   # nested dictionary!
    for k, v in sorted(d['v0001']['days'].items(), key=itemgetter(0), reverse=True):
        if len(k) < 8:
            break
        if 'quality' in d['v0001']['days'][k]:
            for sk,sv in d['v0001']['days'][k]['quality'].items():
                print('quality500.py: ' + str(sk) + ' sv: ' + str(sv))
                if sk not in tquality:
                    tquality[sk] = {}
                    tquality[sk]['count'] = 1
                    tquality[sk]['status'] = sv['status']
                    tquality[sk]['from'] = sv['from']
                    tquality[sk]['comment'] = sv['comment']
                    tquality[sk]['lastoccured'] = k
                else:
                    tquality[sk]['count']  += 1

        if len(tquality) > 0:
            h = "\n\n"
            h += '<div class="row pt-4">' 
            h += '<div class="col-md-12 col-lg-12 col-xxl-6">'
            h += '<h3>Priority 1: Application Errors - Status 500</h3>'
            h += '<p class="card-text">Quality improvements that should be implemented:</p>'
            h += '<table class="table-responsive text-break"><thead><tr><th scope="col">Status</th><th scope="col">affected URL</th><th scope="col">Count</th><th scope="col">Remark</th><th scope="col">Date last occured</th></tr></thead>'
            i = 0
            for k, v in sorted(tquality.items(), key=lambda x: (x[1]['lastoccured']), reverse=True):
                h += '<tr><td>' + str(v['status']) + '</td><td>' + str(k) + "</td>" 
                h += '<td style="text-align: right">' + str(format(v['count'],',')) + '</td>'
                h += '<td>' + v['comment'] + '</td>'
                h += "<td><script>document.write(DT2Locale('" + v['lastoccured'] + "'));</script></td>"
                h += '</tr>'
                if len(v['from']) > 1:
                    h += '<tr><td></td><td colspan="4">called by: ' + v['from'] + '</td></tr>'
                i += 1
                if i == 10:
                    break
            h += '</table>'
            h += '</div></div>'
    return h
