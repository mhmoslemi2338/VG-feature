
################################
# Usage:
#
#   feature is KKFilter(I)
#   I is a grayscale-square-uint8 image
#   Developed by Mohammad Hossein Moslemi: mhmoslemi2338@gmail.com
#   Github: mhmoslemi2338
#
################################



import numpy as np
from itertools import groupby
from collections import Counter

def imageVisibilityGraph(I):
    (n_rows,n_columns)=I.shape
    I=np.int64(I);

    edge_list_index=0
    ei=[]
    ej=[]
    for i in range(1,n_rows+1):
        for j in range(1,n_rows+1):
            if (j<n_columns):
                edge_list_index=edge_list_index+1;
                ei.append(n_columns*(i-1)+j)
                ej.append(n_columns*(i-1)+j+1)
            if(i<n_rows and j<n_columns):
                edge_list_index=edge_list_index+1;
                ei.append(n_columns*(i-1)+j)
                ej.append(n_columns*(i+1-1)+j+1)
            if(i<n_rows):    
                edge_list_index=edge_list_index+1;            
                ei.append(n_columns*(i-1)+j)
                ej.append(n_columns*(i+1-1)+j)
            if(i<n_rows and j>1):
                edge_list_index=edge_list_index+1;            
                ei.append(n_columns*(i-1)+j)
                ej.append(n_columns*(i+1-1)+j-1)

            if(j<n_columns-1):
                k=j+1;
                for c in range(j+2,n_columns+1):
                    cond=1;
                    for l in range(k,c):
                        if((I[i-1,l-1]>=I[i-1,j-1]) or (I[i-1,l-1]>=I[i-1,c-1])):
                            cond=0;
                            k=l;
                            break
                    if(I[i-1,l-1]>=I[i-1,j-1]):
                        break
                    if(cond==1):
                        edge_list_index=edge_list_index+1;
                        ei.append(n_columns*(i-1)+j)
                        ej.append(n_columns*(i-1)+c)
            if(j<n_columns-1 and i<n_rows-1):
                kj=j+1;
                ki=i+1;
                diag_lenght=min(n_rows-i,n_columns-j);
                r=ki;
                for c in range(j+2,j+diag_lenght+1):
                    r=r+1;
                    cond=1;
                    li=ki-1;
                    for lj in range(kj,c):
                        li=li+1;
                        if((I[li-1,lj-1]>=I[i-1,j-1]) or (I[li-1,lj-1]>=I[r-1,c-1])):
                            cond=0;
                            ki=li;
                            kj=lj;
                            break
                    if(I[li-1,lj-1]>=I[i-1,j-1]):
                        break
                    if(cond==1):
                        edge_list_index=edge_list_index+1;
                        ei.append(n_columns*(i-1)+j)
                        ej.append(n_columns*(r-1)+c)
            if(i<n_rows-1):
                k=i+1;
                for r in range(i+2,n_rows+1):
                    cond=1;
                    for l in range(k,r):
                        if((I[l-1,j-1]>=I[i-1,j-1]) or (I[l-1,j-1]>=I[r-1,j-1])):
                            cond=0;
                            k=l;
                            break
                    if(I[l-1,j-1]>=I[i-1,j-1]):
                        break
                    if(cond==1):
                        edge_list_index=edge_list_index+1;
                        ei.append(n_columns*(i-1)+j)
                        ej.append(n_columns*(r-1)+j)
            if(j>2 and i<n_rows-1):
                kj=j-1;
                ki=i+1;
                diag_lenght=min(n_rows-i,j-1);
                c=kj;
                for r in range(i+2,i+diag_lenght+1):
                    c=c-1;
                    cond=1;
                    lj=kj+1;
                    for li in range(ki,r):
                        lj=lj-1;
                        if((I[li-1,lj-1]>=I[i-1,j-1]) or (I[li-1,lj-1]>=I[r-1,c-1])):
                            cond=0;
                            ki=li;
                            kj=lj;
                            break
                    if(I[li-1,lj-1]>=I[i-1,j-1]):
                        break
                    if(cond==1):
                        edge_list_index=edge_list_index+1;
                        ei.append(n_columns*(i-1)+j)
                        ej.append(n_columns*(r-1)+c)

    ei=np.array(ei)
    ej=np.array(ej)
    Edge_list=np.concatenate([ei.reshape(-1,1),ej.reshape(-1,1)],axis=1)
    return Edge_list



def KKFilter(I):
    Edge_list=imageVisibilityGraph(I)
    edge_list_str=[]
    for row in Edge_list:
        edge_list_str.append(str(row[0])+'-'+str(row[1]))
    items = list(vertex for edge in edge_list_str for vertex in edge.split('-'))
    degree = dict(Counter(items))
    degree=dict(sorted(degree.items(), key=lambda kv:int(kv[0])))

    edges = Edge_list.copy()
    edges2=([[row[1],row[0]] for row in edges])
    edges2.sort(key = lambda x : x[0])
    edges2=np.array(edges2)
    tmp=list(np.concatenate([edges,edges2]))
    tmp.sort(key = lambda x : (x[0],x[1]))
    edges=np.array(tmp)
    adj = {k: [v[1] for v in g] for k, g in groupby(edges, lambda e: e[0])}


    kkfilter=[]
    for i in range(1,I.shape[1]*I.shape[0]+1):
        neigh=adj[i]

        tmp=0;
        cnt=0;
        for n1 in neigh:
            tmp=tmp+degree[str(n1)];
            cnt=cnt+1;
        kkfilter.append(round(tmp/cnt))

    kkfilter=np.uint8(kkfilter).reshape(I.shape)
    return kkfilter