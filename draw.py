
from io import BytesIO

import cairo
import IPython.display

def draw(points, rects=[]):
    svgio = BytesIO()
    xmax = max([x for x,_ in points])
    xmin = min([x for x,_ in points])
    ymax = max([y for _,y in points])
    ymin = min([y for _,y in points])
    # inflate by 30% so that everything is in the view
    xmax += 0.3 * (xmax-xmin)
    xmin -= 0.3 * (xmax-xmin)
    ymax += 0.3 * (ymax-ymin)
    ymin -= 1.3 * (ymax-ymin)
    scale = max(xmax-xmin, ymax-ymin)
    
    def transform(points):
        # return [((x-xmin)/(xmax-xmin), (y-ymin)/(ymax-ymin)) for x,y in points]
        return [((x-xmin)/scale, (y-ymin)/scale) for x,y in points]
    newpoints = transform(points)
    with cairo.SVGSurface(svgio, 200, 200) as surface:
        context = cairo.Context(surface)
        context.scale(200, 200)
        context.set_line_width(0.01)
        context.set_font_size(0.03)
        context.move_to(newpoints[0][0], newpoints[0][1])
        for i,(x,y) in enumerate(newpoints[1:]+newpoints[:1]):
            # These lines are copied verbatim from the
            # pycairo page: https://pycairo.readthedocs.io
            x0,y0 = context.get_current_point()
            context.show_text(str(i) + ':' + str((round(points[i][0], 2), round(points[i][1], 2))))
            context.move_to(x0,y0)
#             if i == 0:
#                 context.set_source_rgb(1, 0.2, 0.2)
            context.line_to(x, y)
            context.stroke()
            context.move_to(x,y)
            context.set_source_rgb(0,0,0)
        context.line_to(newpoints[0][0], newpoints[0][1])
        context.stroke()
        for rect in rects:
#             print(rect)
            rect = transform(rect)
            context.move_to(rect[0][0], rect[0][1])
            for x,y in rect[1:]+rect[:1]:
                context.line_to(x,y)
            context.stroke()
    return IPython.display.SVG(data=svgio.getvalue())