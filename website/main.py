from flask import Flask, render_template, request, redirect, session
import mysql.connector as ms

conn = ms.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="rohan",
    database="dbms_proj"
)

if conn.is_connected():
    print("Connected successfully.")

mc = conn.cursor()

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def main_page():
    return render_template("home.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")


@app.route('/login')
def success_page():
    return render_template("login.html")

@app.route('/browse')
def browse_page():
    mc.execute("SELECT a1.name, a2.title from artist a1, artwork a2 WHERE a1.artist_id=a2.artist_id and a2.artwork_id NOT IN (select artwork_id from owns)")
    artists_display_info = mc.fetchall()
    print(artists_display_info)
    artist_1 = artists_display_info[1][0]
    artwork_1 = artists_display_info[1][1]
    artist_2 = artists_display_info[0][0]
    artwork_2 = artists_display_info[0][1]
    
    return render_template("browse.html", artist_1=artist_1, artwork_1=artwork_1, artist_2=artist_2, artwork_2=artwork_2)
    

@app.route('/dashboard', methods=['POST'])
def dashboard_page():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        role = request.form.get('role')  # Assuming a hidden input or URL parameter named 'role'

        # Verify user credentials (consider adding role to this query if it's part of your user table)
        mc.execute("SELECT * FROM user WHERE username=%s AND password=%s", (uname, passwd))
        user_result = mc.fetchall()
        #print(user_result)

        if user_result:
            if role == 'collector':
                # Fetch details from the "collector" table
                mc.execute("SELECT * FROM collector_1 WHERE collector_id=%s", (uname,))
                collector_result = mc.fetchall()
                #print(collector_result)
                
                if collector_result:
                    for collector in collector_result:
                        # Extract needed collector info, assuming similar structure to artist
                        collector_name = collector[1]
                    mc.execute("SELECT * FROM collector_2 WHERE collector_id=%s", (uname, ))
                    collector_result2 = mc.fetchall()
                    
                    collector_contact = [number for _, number in collector_result2]

                    mc.execute("select a1.name, a2.title from collector_1 c1, artwork a2, artist a1, owns o where c1.collector_id = o.collector_id and a2.artwork_id = o.artwork_id and o.collector_id=%s", (uname, ))
                    owns = mc.fetchall()

                    artwork_owned = owns[0][1]
                    by_artist = owns[0][0]
                    
                    mc.execute("SELECT a3.end_date, a3.highest_bid, a2.title FROM auction a3 JOIN artwork a2 ON a3.artwork_id = a2.artwork_id WHERE a3.artwork_id IN (SELECT artwork_id FROM owns WHERE collector_id = %s)", (uname, ))
                    auction_details = mc.fetchall()
                    print(auction_details)
                    auction_date = auction_details[0][0]
                    auction_price = auction_details[0][1]
                    auction_artwork = auction_details[0][2]
                    return render_template("dashboard_collector.html", collector_contact1=collector_contact[0], collector_name=collector_name, collector_contact2=collector_contact[1], artwork_owned=artwork_owned, by_artist=by_artist, auction_date=auction_date, auction_price=auction_price, auction_artwork=auction_artwork)
                else:
                    return "No collector found with that ID.", 404
            elif role == 'artist':
                
                mc.execute("SELECT * FROM artist WHERE artist_id=%s", (uname,))
                artist_result = mc.fetchall()
                print(artist_result)

                for artist in artist_result:
                    artist_name = artist[1]
                    artist_biography = artist[3]
                    artist_portfolio = artist[2]
                
                mc.execute("select a2.title, c1.name from collector_1 c1, artwork a2, owns o where o.artist_id=a2.artist_id and o.collector_id=c1.collector_id and a2.artist_id=%s and a2.artwork_id in (select artwork_id from owns)", (uname, ))
                art_sold_details = mc.fetchall()
                #print(art_sold_details)
                art_title = art_sold_details[0][0]
                art_collector = art_sold_details[0][1]
                return render_template("dashboard_artist.html", artist_name=artist_name, artist_biography=artist_biography, artist_portfolio=artist_portfolio, art_title=art_title, art_collector=art_collector)
        else:
            err = "Invalid username or password!"
            return render_template("login.html", err=err)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
