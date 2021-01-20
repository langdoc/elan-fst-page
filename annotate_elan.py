from flask import *
from elan_fst import *
import os

app = Flask(__name__)

@app.route('/elan-fst/')  
def upload():  
    return render_template("file_upload_form.html")  

@app.route('/elan-fst/success/', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  

        elan_xml = f.stream.read().decode("utf-8")

        root = ET.fromstring(elan_xml)

        tier_structure = detect_tier_structure(root)

        if tier_structure == 'freiburg':

            cg = Cg3("kpv")
            elan_annotated = annotate_freiburg(root, cg = cg)
            ET.ElementTree(elan_annotated).write("temp.eaf", xml_declaration=True, encoding='utf-8', method="xml")

        if tier_structure == 'oulu':

            cg = Cg3("smn")
            elan_annotated = annotate_oulu(root, cg = cg)
            ET.ElementTree(elan_annotated).write("temp.eaf", xml_declaration=True, encoding='utf-8', method="xml")

        table = print_unknown_words("temp.eaf")

        return render_template("success.html", name = f.filename, table = table)  

@app.route('/elan-fst/return-files/')
def return_files():
    try:
#        f = request.files['file']
        return send_file('temp.eaf',  mimetype='application/xml', attachment_filename="test.eaf", as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':  
    app.run()

#@app.route("/", methods=['POST'])
#elan_file_path = sys.argv[1]
#with open(elan_file_path, 'r') as file:
#    elan_xml = file.read()

#root = ET.fromstring(elan_xml)

#elan_tokenized = tokenize_elan(root, 
#                              target_type = 'word token', 
#                              orig_tier_part = 'orth', 
#                              new_tier_part = 'word', 
#                              process = word_tokenize)

#cg = Cg3("smn")
#elan_annotated = annotate_elan(elan_tokenized, cg = cg)

#ET.ElementTree(elan_annotated).write(sys.argv[2], xml_declaration=True, encoding='utf-8', method="xml")

#! xmllint --format - < /Users/niko/github/oulu-elan/test.eaf > /Users/niko/github/oulu-elan/test-pretty.eaf
#! xmllint --noout --schema /Users/niko/github/oulu-elan/EAFv3.0.xsd /Users/niko/github/oulu-elan/test-pretty.eaf
