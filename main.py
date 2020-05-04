from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response
from customer import customerList
from venue import venueList
from event import eventList
from ticket import ticketList
import pymysql,json,time

from flask_session import Session  #serverside sessions

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])

@app.route('/login',methods = ['GET','POST'])
def login():
    '''
    -check login
    -set session
    -redirect to menu
    -check session on login pages
    '''
    if request.form.get('email') is not None and request.form.get('password') is not None:
        c = customerList()
        if c.tryLogin(request.form.get('email'),request.form.get('password')):
            print('login ok')
            session['user'] = c.data[0]
            session['active'] = time.time()

            return redirect('main')
        else:
            print('login failed')
            return render_template('login.html', title='Login', msg='Incorrect login.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)
@app.route('/logout',methods = ['GET','POST'])
def logout():
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', msg='Logged out.')
@app.route('/nothing')
def nothing():
    print('hi')
    return ''

@app.route('/basichttp')
def basichttp():
    if request.args.get('myvar') is not None:
        a = request.args.get('myvar')
        return 'your var:' + request.args.get('myvar')
    else:
        return 'myvar not set'

@app.route('/')
def home():
    return redirect('login')
    #return render_template('test.html', title='Test2', msg='Welcome!')

@app.route('/index')
def index():
    user = {'username': 'Tyler'}


    items = [
        {'name':'Apple','price':2.34},
        {'name':'Orange','price':4.88},
        {'name':'Grape','price':2.44}
    ]
    return render_template('index.html', title='Home', user=user, items=items)
@app.route('/customers')
def customers():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    c.getAll()

    print(c.data)
    #return ''
    return render_template('customers.html', title='Customer List',  customers=c.data)

@app.route('/customer')
def customer():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    if request.args.get(c.pk) is None:
        return render_template('error.html', msg='No customer id given.')

    c.getById(request.args.get(c.pk))
    if len(c.data) <= 0:
        return render_template('error.html', msg='Customer not found.')

    print(c.data)
    return render_template('customer.html', title='Customer ',  customer=c.data[0])

@app.route('/newcustomer',methods = ['GET', 'POST'])
def newcustomer():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('fname') is None:
        c = customerList()
        c.set('fname','')
        c.set('lname','')
        c.set('email','')
        c.set('password','')
        c.set('address','')
        c.set('phonenumber','')
        c.set('admin','')
        c.add()
        return render_template('newcustomer.html', title='New Customer',  customer=c.data[0])
    else:
        c = customerList()
        c.set('fname',request.form.get('fname'))
        c.set('lname',request.form.get('lname'))
        c.set('email',request.form.get('email'))
        c.set('address',request.form.get('address'))
        c.set('phonenumber',request.form.get('phonenumber'))
        c.set('password',request.form.get('password'))
        c.set('admin',request.form.get('admin'))
        c.add()
        if c.verifyNew():
            c.insert()
            print(c.data)
            return render_template('savedcustomer.html', title='Customer Saved',  customer=c.data[0])
        else:
            return render_template('newcustomer.html', title='Customer Not Saved',  customer=c.data[0],msg=c.errorList)
@app.route('/savecustomer',methods = ['GET', 'POST'])
def savecustomer():
    if checkSession() == False:
        return redirect('login')
    c = customerList()
    c.set('UID',request.form.get('UID'))
    c.set('fname',request.form.get('fname'))
    c.set('lname',request.form.get('lname'))
    c.set('email',request.form.get('email'))
    c.set('address',request.form.get('address'))
    c.set('phonenumber',request.form.get('phonenumber'))
    c.set('password',request.form.get('password'))
    c.set('admin',request.form.get('admin'))
    c.add()
    c.update()
    print(c.data)
    #return ''
    return render_template('savedcustomer.html', title='Customer Saved',  customer=c.data[0])

@app.route('/deletecustomer',methods = ['GET', 'POST'])
def deletecustomer():
    if checkSession() == False:
        return redirect('login')
    print("UID:",request.form.get('UID'))
    #return ''
    c = customerList()
    c.deleteById(request.form.get('UID'))
    return render_template('confirmaction.html', title='Customer Deleted',  msg='Customer deleted.')
'''
================================================================================================================================================================
START VENUE PAGES
================================================================================================================================================================
'''

@app.route('/venues')
def venues():
    v = venueList()
    v.getAll()

    #print(c.data)
    #return ''
    return render_template('venue/venues.html', title='Venue List', venues=v.data)

@app.route('/venue')
def onevenue():
    if checkSession() == False:
        return redirect('login')
    v = venueList()
    if request.args.get('id') is None:
        return render_template('error.html', msg='No venue id given')

    v.getById(request.args.get('id'))
    if len(v.data) <= 0:
        return render_template('error.html', msg='Venue not found')

    print(v.data)
    return render_template('venue/venue.html', title='Venue', venue=v.data[0])

@app.route('/newvenue',methods = ['GET', 'POST'])
def newvenue():
    if checkSession() == False:
        return redirect('login')
    if request.form.get('VenueName') is None:
        v = venueList()
        v.set('VenueName','')
        v.set('VenueAddress','')
        v.set('VenueCollege','')
        v.set('VenuePhoneNumber','')
        v.add()
        return render_template('venue/newvenue.html', title='New Venue', venue=v.data[0])
    else:
        v = venueList()
        v.set('VenueName',request.form.get('VenueName'))
        v.set('VenueAddress',request.form.get('VenueAddress'))
        v.set('VenueCollege',request.form.get('VenueCollege'))
        v.set('VenuePhoneNumber',request.form.get('VenuePhoneNumber'))
        v.add()
        if v.verifyNew():
            v.insert()
            return render_template('venue/savedvenue.html', title='Venue Saved', venue=v.data[0])
        else:
            return render_template('venue/newvenue.html', title='Venue Not Saved', venue=v.data[0],msg=v.errorList)

@app.route('/savevenue',methods = ['GET', 'POST'])
def savevenue():
    if checkSession() == False:
        return redirect('login')
    v = venueList()
    v.set('VenueID',request.form.get('VenueID'))
    v.set('VenueName',request.form.get('VenueName'))
    v.set('VenueAddress',request.form.get('VenueAddress'))
    v.set('VenueCollege',request.form.get('VenueCollege'))
    v.set('VenuePhoneNumber',request.form.get('VenuePhoneNumber'))
    v.add()
    v.update()
    print(v.data)
    return render_template('venue/savedvenue.html', title='Venue Saved', venue=v.data[0])

@app.route('/deletevenue',methods = ['GET', 'POST'])
def deletevenue():
    if checkSession() == False:
        return redirect('login')
    print("VenueID:",request.form.get('VenueID'))
    #return ''
    v = venueList()
    v.deleteById(request.form.get('VenueID'))
    return render_template('confirmaction.html', title='Venue Deleted',  msg='Venue deleted.')

'''
================================================================================================================================================================
END VENUE PAGES
================================================================================================================================================================
'''

'''
================================================================================================================================================================
START EVENT PAGES
================================================================================================================================================================
'''

@app.route('/events')
def events():
    allVenues = venueList()
    allVenues.getAll()
    e = eventList()
    e.getAll()

    #print(c.data)
    #return ''
    return render_template('event/events.html', title='Event List', events=e.data,vl=allVenues.data)

@app.route('/event')
def oneevent():
    if checkSession() == False:
        return redirect('login')
    allVenues = venueList()
    allVenues.getAll()
    e = eventList()
    if request.args.get('id') is None:
        return render_template('error.html', msg='No event id given')

    e.getById(request.args.get('id'))
    if len(e.data) <= 0:
        return render_template('error.html', msg='Event not found')

    print(e.data)
    return render_template('event/event.html', title='Event', event=e.data[0], vl=allVenues.data)

@app.route('/newevent',methods = ['GET', 'POST'])
def newevent():
    if checkSession() == False:
        return redirect('login')
    allVenues = venueList()
    allVenues.getAll()
    if request.form.get('name') is None:
        e = eventList()
        e.set('VenueID','')
        e.set('name','')
        e.set('start','')
        e.set('end','')
        e.add()
        return render_template('event/newevent.html', title='New Event', event=e.data[0], vl=allVenues.data)
    else:
        e = eventList()
        e.set('VenueID',request.form.get('VenueID'))
        e.set('name',request.form.get('name'))
        e.set('start',request.form.get('start'))
        e.set('end',request.form.get('end'))
        e.add()
        if e.verifyNew():
            e.insert()
            return render_template('event/savedevent.html', title='Event Saved', event=e.data[0], vl=allVenues.data)
        else:
            return render_template('event/newevent.html', title='Event Not Saved', event=e.data[0],msg=e.errorList, vl=allVenues.data)

@app.route('/saveevent',methods = ['GET', 'POST'])
def saveevent():
    if checkSession() == False:
        return redirect('login')
    else:
        e = eventList()
        e.set('VenueID',request.form.get('VenueID'))
        e.set('EID',request.form.get('Event ID'))
        e.set('name',request.form.get('Event Name'))
        e.set('start',request.form.get('Event Start'))
        e.set('end',request.form.get('Event End'))
        e.add()
        e.update()
        print(e.data)
        return render_template('event/savedevent.html', title='Event Saved', event=e.data[0])

@app.route('/deleteevent',methods = ['GET', 'POST'])
def deleteevent():
    if checkSession() == False:
        return redirect('login')
    print("EID:",request.form.get('EID'))
    #return ''
    e = eventList()
    e.deleteById(request.form.get('EID'))
    return render_template('confirmaction.html', title='Event Deleted',  msg='Event deleted.')


'''
================================================================================================================================================================
END EVENT PAGES
================================================================================================================================================================
'''

'''
================================================================================================================================================================
START TICKETS PAGES
================================================================================================================================================================
'''
@app.route('/tickets')
def tickets():
    t = ticketList()
    t.getByCustomer(session['user']['UID'])

    #print(c.data)
    #return ''
    return render_template('ticket/tickets.html', title='Ticket List', tickets=t.data)

@app.route('/ticket')
def oneticket():
    if checkSession() == False:
        return redirect('login')
    allEvents = eventList()
    allEvents.getAll()
    t = ticketList()
    if request.args.get('id') is None:
        return render_template('error.html', msg='No ticket id given')

    t.getById(request.args.get('id'))
    if len(t.data) <= 0:
        return render_template('error.html', msg='Ticket not found')

    print(t.data)
    return render_template('ticket/ticket.html', title='Ticket', ticket=t.data[0],el=allEvents.data)

@app.route('/newticket',methods = ['GET', 'POST'])
def newticket():
    if checkSession() == False:
        return redirect('login')
    allEvents = eventList()
    allEvents.getAll()
    if request.form.get('section') is None:
        t = ticketList()
        t.set('EventID','')
        t.set('section','')
        t.set('row','')
        t.set('available','')
        t.set('handicap','')
        t.set('type','')
        t.set('box','')
        t.set('UserID','')
        t.add()
        return render_template('ticket/newticket.html', title='New Ticket', ticket=t.data[0],el=allEvents.data)
    else:
        t = ticketList()
        t.set('EventID',request.form.get('EventID'))
        t.set('section',request.form.get('section'))
        t.set('row',request.form.get('row'))
        t.set('available',request.form.get('available'))
        t.set('handicap',request.form.get('handicap'))
        t.set('type',request.form.get('type'))
        t.set('box',request.form.get('box'))
        t.set('UserID',session['user']['UID'])
        t.add()
        if t.verifyNew():
            t.insert()
            return render_template('ticket/savedticket.html', title='Ticket Saved', ticket=t.data[0], el=allEvents.data)
        else:
            return render_template('ticket/newticket.html', title='Ticket Not Saved', ticket=t.data[0],msg=t.errorList, el=allEvents.data)

@app.route('/saveticket',methods = ['GET', 'POST'])
def saveticket():
    if checkSession() == False:
        return redirect('login')
    t = ticketList()
    t.set('TID',request.form.get('TID'))
    t.set('EventID',request.form.get('EventID'))
    t.set('section',request.form.get('section'))
    t.set('row',request.form.get('row'))
    t.set('available',request.form.get('available'))
    t.set('handicap',request.form.get('handicap'))
    t.set('type',request.form.get('type'))
    t.set('box',request.form.get('box'))
    t.set('UserID',session['user']['UID'])
    t.add()
    t.update()
    print(t.data)
    return render_template('ticket/savedticket.html', title='Ticket Saved', ticket=t.data[0])

@app.route('/mytickets')
def mytickets():
    if checkSession() == False:
        return redirect('login')
    t = ticketList()
    t.getByCustomer(session['user']['UID'])

    print(t.data)
    #return ''
    return render_template('ticket/mytickets.html', title='My tickets',  tickets=t.data)

@app.route('/alltickets')
def alltickets():
    if checkSession() == False:
        return redirect('login')
    allEvents = eventList()
    allEvents.getAll()
    t = ticketList()
    t.getAll()

    print(t.data)
    #return ''
    return render_template('ticket/tickets.html', title='My tickets',  tickets=t.data, el=allEvents.data)

@app.route('/admintickets')
def admintickets():
    if checkSession() == False:
        return redirect('login')
    allEvents = eventList()
    allEvents.getAll()
    t = ticketList()
    t.getByCustomer(session['user']['UID'])

    print(t.data)
    #return ''
    return render_template('ticket/mytickets.html', title='My tickets',  tickets=t.data, el=allEvents.data)

'''
================================================================================================================================================================
END TICKETS PAGES
================================================================================================================================================================
'''

'''
================================================================================================================================================================
END CUSTOMER PAGES
================================================================================================================================================================
'''
@app.route('/customerevents')
def customerevents():
    allVenues = venueList()
    allVenues.getAll()
    e = eventList()
    e.getAll()

    #print(c.data)
    #return ''
    return render_template('event/customerevents.html', title='Event List', events=e.data, vl=allVenues.data)

@app.route('/customervenues')
def customervenues():
    v = venueList()
    v.getAll()

    #print(c.data)
    #return ''
    return render_template('venue/customervenues.html', title='Venue List', venues=v.data)

@app.route('/customerticket')
def customerticket():
    allEvents = eventList()
    allEvents.getAll()
    t = ticketList()
    t.getByCustomer(session['user']['UID'])

    #print(c.data)
    #return ''
    return render_template('ticket/customerticket.html', title='Ticket List', tickets=t.data,el=allEvents.data)

@app.route('/customertickets')
def customertickets():
    allEvents = eventList()
    allEvents.getAll()
    t = ticketList()
    t.getByCustomer(session['user']['UID'])

    #print(c.data)
    #return ''
    return render_template('ticket/customertickets.html', title='Ticket List', tickets=t.data, el=allEvents.data)

@app.route('/newcustomerticket',methods = ['GET', 'POST'])
def newcustomerticket():
    if checkSession() == False:
        return redirect('login')
    allEvents = eventList()
    allEvents.getAll()
    if request.form.get('section') is None:
        t = ticketList()
        t.set('EventID','')
        t.set('section','')
        t.set('row','')
        t.set('available','')
        t.set('handicap','')
        t.set('type','')
        t.set('box','')
        t.set('UserID','')
        t.add()
        return render_template('ticket/newticket.html', title='New Ticket', ticket=t.data[0],el=allEvents.data)
    else:
        t = ticketList()
        t.set('EventID',request.form.get('EventID'))
        t.set('section',request.form.get('section'))
        t.set('row',request.form.get('row'))
        t.set('available',request.form.get('available'))
        t.set('handicap',request.form.get('handicap'))
        t.set('type',request.form.get('type'))
        t.set('box',request.form.get('box'))
        t.set('UserID',session['user']['UID'])
        t.add()
        if t.verifyNew():
            t.insert()
            return render_template('ticket/savedticket.html', title='Ticket Saved', ticket=t.data[0], el=allEvents.data)
        else:
            return render_template('ticket/newticket.html', title='Ticket Not Saved', ticket=t.data[0],msg=t.errorList, el=allEvents.data)

'''
================================================================================================================================================================
END CUSTOMER PAGES
================================================================================================================================================================
'''

@app.route('/main')
def main():
    if checkSession() == False:
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['fname']
    if session['user']['admin'] == 'True':
        return render_template('main.html', title='Admin menu',msg = userinfo)
    elif session['user']['admin'] == 'False':
        return render_template('maincustomer.html', title='Customer menu',msg = userinfo)
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
