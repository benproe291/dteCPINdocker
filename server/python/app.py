from flask import Flask, request, render_template
import sys
sys.path.insert(0, 'webpage\python\model291.py')
import model291

app = Flask(__name__)

