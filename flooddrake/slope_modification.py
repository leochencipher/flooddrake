from __future__ import division
from __future__ import absolute_import

from firedrake import *


def SlopeModification(w):
    """ Slope modification for the prevention of non negative flows in some verticies of cells. This is from Ern et al (2011)

        :param w: state vector

    """

    V = w.function_space()

    if V.mesh().geometric_dimension() == 2:

        # split functions
        h, mu, mv = split(w)

        # split function spaces
        v, vu, vv = split(V)

    if V.mesh().geometric_dimension() == 1:

        # split functions
        h, mu = split(w)

        # split function spaces
        v, vu = split(V)

    slope_modification_2d_kernel = """ double new_cell = 0; const E=1e-6, UB=1e0; int j;
    for(int i=0;i<vert_cell.dofs;i++){
        new_cell+=vert_cell[i][0];
    }
    new_cell=new_cell/vert_cell.dofs;
    if (new_cell<=E){
        for(int i=0;i<new_vert_cell.dofs;i++){
            new_vert_cell[i][0]=0;
            new_vert_u_cell[i][0]=0;
            new_vert_v_cell[i][0]=0;
        }
    }
    if (new_cell>E){
        float c=0;
        for(int i=0;i<new_vert_cell.dofs;i++){
            if (vert_cell[i][0]>E){
                new_vert_cell[i][0]=vert_cell[i][0];
                new_vert_u_cell[i][0]=vert_u_cell[i][0];
                new_vert_v_cell[i][0]=vert_v_cell[i][0];
            }
            if (vert_cell[i][0]<=E){
                c=c+1;
                j=i;
            }
        }
        if (c==0){
            for(int i=0;i<new_vert_cell.dofs;i++){
                if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                    new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                }
                if (new_vert_v_cell[i][0]/new_vert_cell[i][0]>UB){
                    new_vert_v_cell[i][0]=UB*new_vert_cell[i][0];
                }
                if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                    new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                }
                if ((new_vert_v_cell[i][0]/new_vert_cell[i][0])<-UB){
                    new_vert_v_cell[i][0]=(-UB)*new_vert_cell[i][0];
                }
            }
        }
        if (c==1){
            for(int i=0;i<new_vert_cell.dofs;i++){
                new_vert_cell[i][0]=(new_cell/(new_cell-vert_cell[j][0]))*(vert_cell[i][0]-vert_cell[j][0]);
                if (new_vert_cell[i][0]>0){
                    if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if (new_vert_v_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_v_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                    if ((new_vert_v_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_v_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                }
            }
            new_vert_u_cell[j][0]=0;
            new_vert_v_cell[j][0]=0;
        }
        if (c==2){
            for(int i=0;i<new_vert_cell.dofs;i++){
                if (vert_cell[i][0]<=E){
                    new_vert_cell[i][0]=0;
                    new_vert_u_cell[i][0]=0;
                    new_vert_v_cell[i][0]=0;
                }
                if (vert_cell[i][0]>E){
                    new_vert_cell[i][0]=new_cell*3;
                    if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if (new_vert_v_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_v_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                    if ((new_vert_v_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_v_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                }
            }
        }
    }
    """

    slope_modification_1d_kernel = """ double new_cell = 0; const E=1e-6, UB=1e0; int j;
    for(int i=0;i<vert_cell.dofs;i++){
        new_cell+=vert_cell[i][0];
    }
    new_cell=new_cell/vert_cell.dofs;
    if (new_cell<=E){
        for(int i=0;i<new_vert_cell.dofs;i++){
            new_vert_cell[i][0]=0;
            new_vert_u_cell[i][0]=0;
        }
    }
    if (new_cell>E){
        float c=0;
        for(int i=0;i<new_vert_cell.dofs;i++){
            if (vert_cell[i][0]>E){
                new_vert_cell[i][0]=vert_cell[i][0];
                new_vert_u_cell[i][0]=vert_u_cell[i][0];
            }
            if (vert_cell[i][0]<=E){
                c=c+1;
                j=i;
            }
        }
        if (c==0){
            for(int i=0;i<new_vert_cell.dofs;i++){
                if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                    new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                }
                if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                    new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                }
            }
        }
        if (c==1){
            for(int i=0;i<new_vert_cell.dofs;i++){
                new_vert_cell[i][0]=(new_cell/(new_cell-vert_cell[j][0]))*(vert_cell[i][0]-vert_cell[j][0]);
                if (new_vert_cell[i][0]>0){
                    if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                }
            }
            new_vert_u_cell[j][0]=0;
        }
        if (c==2){
            for(int i=0;i<new_vert_cell.dofs;i++){
                if (vert_cell[i][0]<=E){
                    new_vert_cell[i][0]=0;
                    new_vert_u_cell[i][0]=0;
                }
                if (vert_cell[i][0]>E){
                    new_vert_cell[i][0]=new_cell*3;
                    if (new_vert_u_cell[i][0]/new_vert_cell[i][0]>UB){
                        new_vert_u_cell[i][0]=UB*new_vert_cell[i][0];
                    }
                    if ((new_vert_u_cell[i][0]/new_vert_cell[i][0])<-UB){
                        new_vert_u_cell[i][0]=(-UB)*new_vert_cell[i][0];
                    }
                }
            }
        }
    }
    """

    nf = Function(V)

    if V.mesh().geometric_dimension() == 2:
        new_v_func, new_v_u_func, new_v_v_func = split(nf)

    if V.mesh().geometric_dimension() == 1:
        new_v_func, new_v_u_func = split(nf)

    # par loop

    if V.mesh().geometric_dimension() == 2:
        par_loop(slope_modification_2d_kernel, dx, {
            "new_vert_v_cell": (new_v_v_func, RW),
            "new_vert_u_cell": (new_v_u_func, RW),
            "new_vert_cell": (new_v_func, RW),
            "vert_cell": (h, READ),
            "vert_u_cell": (mu, READ),
            "vert_v_cell": (mv, READ)
        })

    if V.mesh().geometric_dimension() == 1:
        par_loop(slope_modification_1d_kernel, dx, {
            "new_vert_u_cell": (new_v_u_func, RW),
            "new_vert_cell": (new_v_func, RW),
            "vert_cell": (h, READ),
            "vert_u_cell": (mu, READ)
        })

    return nf