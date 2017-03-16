#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


    def post(self):
        stevilo1 = float(self.request.get("stevilo1"))
        znak = self.request.get("znak")
        stevilo2 = float(self.request.get("stevilo2"))

        rezultat = ""

        if znak == "+":
            rezultat = stevilo1 + stevilo2
        elif znak == "-":
            rezultat = stevilo1 - stevilo2
        elif znak == "/":
            rezultat = stevilo1 / stevilo2
        elif znak == "*":
            rezultat = stevilo1 * stevilo2


        return self.write("Rezultat je %s" % rezultat)


class SteviloHandler(BaseHandler):
    def get(self):
        return self.render_template("skritostevilo.html")

    def post(self):
        resitev = 7
        odgovor = int(self.request.get("skrito"))


        if resitev == odgovor:
            return self.write("Tvoj odgovor je pravilen tvoje skrito stevilo je 7")
        elif resitev > odgovor:
            return self.write("Tvoj odgovor je prenizek")
        elif resitev < odgovor:
            return self.write("Tvoj odgovor je previsok")

class PretvornikHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornikenot.html")

    def post(self):
        kilometri = float(self.request.get("pretvornik"))
        milje = 0.62137 * kilometri
        return self.write(milje)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/skritostevilo', SteviloHandler),
    webapp2.Route('/pretvornikenot',PretvornikHandler),
], debug=True)