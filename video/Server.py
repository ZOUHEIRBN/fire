from flask import Flask, render_template, Response, request
from data import DataSource as ds
from video import effects as eff
from actors.agents import AlertSystem, FetchAgent
from actors.user import User
import webbrowser


class Server(Flask):
    def __init__(self, host='0.0.0.0', port=5001, system=None):
        super(Server, self).__init__(__name__, template_folder='../templates', static_folder='../static')
        self.RTData = ds.RealTimeData(server=self)
        self.host = host
        self.port = port

        if system is not None:
            self.system = system
        else:
            self.system = AlertSystem(server=self)


        self.add_url_rule('/', view_func=self.default_page)
        self.add_url_rule('/auth', view_func=self.authenticate, methods=["POST", "GET"])
        if self.host == '0.0.0.0':
            webbrowser.open('http://127.0.0.1:'+str(self.port)+'/')
        else:
            webbrowser.open('http://'+self.host+':'+str(self.port)+'/')


    def __del__(self):
        self.RTData.source.__feed__.release()

    def default_page(self):
        return render_template('default.html')

    def visualizer(self):
        print()
        params = {'Cam': [f.replace('_', ' ').title() for f in dir(eff) if not (f.startswith('__') and f.endswith('__')) and f not in ['cv2', 'np']],
                  'Ptypes': ['Bar', 'Derived', 'Plot']}

        self.RTData = ds.RealTimeData(server=self)

        def func():
            return float(self.RTData.state["Fire"])

        self.awake_agent = FetchAgent(unique_id=0, model=self.system, func=func)
        self.awake_agent.set_threshold(0)

        self.add_url_rule('/video_feed', view_func=self.video_feed, methods=["POST", "GET"])
        self.add_url_rule('/graph_feed', view_func=self.graph_feed, methods=["POST", "GET"])
        self.add_url_rule('/score_feed', view_func=self.score_feed, methods=["POST", "GET"])
        self.add_url_rule('/notif_feed', view_func=self.notif_feed, methods=["POST", "GET"])
        self.add_url_rule('/realtime_feed', view_func=self.data_feed, methods=["POST", "GET"])
        return render_template('visualizer.html', **params)

    def authenticate(self):
        usrs = User.get_users_data()
        if request.method == "POST" or True:
            result = request.form
            usr = result['username']
            passwd = result['password']

            for e in usrs:
                if e["User"] == usr and e["Pass"] == passwd:
                    self.add_url_rule('/viz', view_func=self.visualizer)
                    return str(e["id"])

        return str(-1)

    def data_gen(self):
        while True:
            data = self.RTData.to_dict()
            if True:
                pass
            d_json = data.json()
            yield d_json

    def graph_gen(self, source=0):
        if source == 0:
            source = self.RTData.sensor_plot
        while True:
            source.refresh()
            frame = source.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def score_graph_gen(self, source=0):
        if source == 0:
            source = self.RTData.state_plot
        while True:
            source.refresh()
            frame = source.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_gen(self, source=0):
        """Video streaming generator function."""
        if source==0:
            source = self.RTData.source
        while True:
            frame = source.get_frame()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    #Video feed
    def video_feed(self):
        if request.method == 'POST':
            value = request.form['value'].replace(' ', '_').lower()
            self.RTData.source.__effect__ = getattr(eff, value)
            return "Changing video device"

        return Response(self.video_gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    #Graph feed
    def graph_feed(self):
        if request.method == 'POST':
            value = request.form['value']
            self.RTData.sensor_plot.refresh(vtype=value)
            return "Changing plot type"

        return Response(self.graph_gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    #Certitude  feed
    def score_feed(self):
        if request.method == 'POST':
            value = request.form['value']
            self.RTData.state_plot.refresh(vtype=value)
            return "Changing plot type"

        return Response(self.score_graph_gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    #Data feed
    def data_feed(self):
        if request.method == 'GET':
            return Response(self.RTData.json(),
                        mimetype='text/plain')

    #Notif feed
    def notif_feed(self):
        if request.method == 'GET':
            self.awake_agent.step()
            return Response(str(self.awake_agent.message),
                            mimetype='text/plain')

    def run(self, **options):
        super(Server, self).run(host=self.host, port=self.port, debug=self.debug)


if __name__ == '__main__':
    #"""
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    #"""

    app = Server(port=3030)
    app.run()