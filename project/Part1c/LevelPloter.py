import numpy as np
import cairo as cr

class LevelPloter(object):
    def __init__(self,
                 outfile,
                 energies,
                 j,width=100,
                 height=200,
                 border = 20,
                 min_e = -1,
                 max_e = 6,
                 num_tics = 8):
        self.energies = (energies-np.min(energies))
        self.j = j
        self.width = width
        self.height = height
        self.border = border
        self.cairo_surf = cr.PSSurface(open(outfile,"w"),width+border*2,height+border*2)
        self.min_e = min_e
        self.max_e = max_e
        self.num_tics = num_tics
        
    def plotLevels(self):
        cairo_context = cr.Context(self.cairo_surf)
        cairo_context.set_line_width(0.1)
        cairo_context.set_font_size(4.0)
        cairo_context.translate(self.border,self.border)
        cairo_context.rectangle(0,0,self.width,self.height)
        e_scale = self.height/(self.max_e-self.min_e)
        j_scale = self.width/(np.max(self.j)-np.min(self.j)+3)
        # Draw E-axis
        for itic in range(1,self.num_tics):
            etic = self.min_e+(itic)*(self.max_e-self.min_e)/(float(self.num_tics)-1)
            y = self.height-(etic-self.min_e)*e_scale
            cairo_context.move_to(0,y)
            cairo_context.line_to(0.3*j_scale,y)
            tex = "{}".format(etic)
            cairo_context.move_to(-0.5*j_scale*(0.05+len(tex)/2.0),y)
            cairo_context.show_text(tex)
            
        for i,e in enumerate(self.energies):
            if (e<self.min_e):
                continue
            if (e>self.max_e):
                break
            y = self.height-(e-self.min_e)*e_scale
            cairo_context.move_to(j_scale*0.5,y)
            cairo_context.line_to(j_scale*(self.j[i]+1),y)
            if (int(2*self.j[i]+0.5) == 2*int(self.j[i]+0.5)):
                cairo_context.show_text("{}+".format(int(self.j[i]+0.5)))
            else:
                cairo_context.show_text("{}/2+".format(int(2*self.j[i]+0.5)))
        cairo_context.stroke()
        self.cairo_surf.flush()
