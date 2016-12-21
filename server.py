# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import cobiss
app = Flask(__name__)

@app.route("/")
def template_test():
    return render_template('index.html')

@app.route('/url', methods=['POST'])
def parse_request():
    url = request.form.get('url')
    podatki = cobiss.prenesiPodatkeOKnjigi(url)
    return render_template('podatki.html', naslov=podatki["naslov"])
    
if __name__ == '__main__':
    app.run("0.0.0.0", 80, debug=True)
