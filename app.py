""" web app to find the stock price for current month """


from flask import Flask, render_template,request


app=Flask(__name__)


#home page
@app.route('/')
def home():
    return render_template("home.html")



#search page
@app.route('/search/')
def search():
    return render_template("search.html")



#plot page
@app.route('/plot/', methods=['POST'])
def plot():
    from pandas_datareader import data
    from datetime import datetime as dt
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN
    import calendar



    #getting the data using pandas data reader
    if request.method=='POST':
        stockname=request.form["stock_name"]
        month=request.form["month"]
        
        my_date = dt.strptime(month, "%Y-%m")
        md1=calendar.monthrange(my_date.year,my_date.month)

        stockname=str(stockname)
        stockname=stockname.upper()
        start=my_date.date()
        end=dt(my_date.year,my_date.month,md1[1])

        try:

            #storing the data collected in a df dataframe
            df=data.DataReader(name=stockname,data_source="yahoo",start=start,end=end) 
            def stat(c,o):
                if c > o:
                    value="Increase"
                elif o > c:
                    value="Decrease"
                else:
                    value="Equal"
                return value



            df["Status"]=[stat(c,o) for c,o in zip(df.Close,df.Open)]
            df["Middle"]=(df.Open+df.Close)/2
            df["Height"]=abs(df.Open-df.Close)
            p= figure(x_axis_type='datetime',width=1000,height=300)
            p.title.text=stockname
            p.grid.grid_line_alpha=0.8
            p.segment(df.index,df.High,df.index,df.Low,color="Black")
            hours_12=12*60*60*1000
            p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],
            hours_12, df.Height[df.Status=="Increase"],fill_color="MediumSeaGreen",line_color="black")
            p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],hours_12,df.Height[df.Status=="Decrease"],fill_color="#ff6347",line_color="black")
            

            #getting the html and jason files components of the plot
            script1,div1=components(p)
            cdn_js=CDN.js_files[0]
            
            df.drop(["Middle", "Height"], axis = 1, inplace = True)

            return render_template("plot.html",
            script1=script1,
            div1=div1,
            cdn_js=cdn_js,text=df.to_html(), btn="download.html")
        except:
             return render_template("search.html", text="Seems like we got wrong stock name")




if __name__=="__main__":
    app.run(debug=True)
