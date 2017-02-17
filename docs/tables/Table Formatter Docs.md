
# HTML Tables and Table Formatting


## Creating a HTML Table from pandas.DataFrame
The following is hopefully sufficient for most applications (feedback welcome!):
```
from pybloqs import Blockb = Block(df)
```

When called only with DataFrame as parameter, a set of default formatters is applied: 
```
table_block = Block(df, formatters=None, use_default_formatters=True)
```


    import pybloqs as abl
    from pybloqs import Block
    import pandas as pd
    import numpy as np
    df = pd.DataFrame(np.random.rand(4,4), index=['a','b','c','d'], columns = ['aa','bb','cc','dd'])
    df.index.name = 'ABC'
    table_block = Block(df)
    output = table_block.render_html()
    
    
    # Displaying pybloqs out in jupyter requires rendering html output
    from IPython.core.display import display, HTML
    display(HTML(output))


<!DOCTYPE html>
<html>
 <head>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_jsinflate) == 'undefined'){(function(){var zip_WSIZE=32768;var zip_STORED_BLOCK=0;var zip_STATIC_TREES=1;var zip_DYN_TREES=2;var zip_lbits=9;var zip_dbits=6;var zip_INBUFSIZ=32768;var zip_INBUF_EXTRA=64;var zip_slide;var zip_wp;var zip_fixed_tl=null;var zip_fixed_td;var zip_fixed_bl,fixed_bd;var zip_bit_buf;var zip_bit_len;var zip_method;var zip_eof;var zip_copy_leng;var zip_copy_dist;var zip_tl,zip_td;var zip_bl,zip_bd;var zip_inflate_data;var zip_inflate_pos;var zip_MASK_BITS=new Array(0x0000,0x0001,0x0003,0x0007,0x000f,0x001f,0x003f,0x007f,0x00ff,0x01ff,0x03ff,0x07ff,0x0fff,0x1fff,0x3fff,0x7fff,0xffff);var zip_cplens=new Array(3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258,0,0);var zip_cplext=new Array(0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,99,99);var zip_cpdist=new Array(1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577);var zip_cpdext=new Array(0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13);var zip_border=new Array(16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15);var zip_HuftList=function(){this.next=null;this.list=null;}
var zip_HuftNode=function(){this.e=0;this.b=0;this.n=0;this.t=null;}
var zip_HuftBuild=function(b,n,s,d,e,mm){this.BMAX=16;this.N_MAX=288;this.status=0;this.root=null;this.m=0;{var a;var c=new Array(this.BMAX+1);var el;var f;var g;var h;var i;var j;var k;var lx=new Array(this.BMAX+1);var p;var pidx;var q;var r=new zip_HuftNode();var u=new Array(this.BMAX);var v=new Array(this.N_MAX);var w;var x=new Array(this.BMAX+1);var xp;var y;var z;var o;var tail;tail=this.root=null;for(i=0;i<c.length;i++)
c[i]=0;for(i=0;i<lx.length;i++)
lx[i]=0;for(i=0;i<u.length;i++)
u[i]=null;for(i=0;i<v.length;i++)
v[i]=0;for(i=0;i<x.length;i++)
x[i]=0;el=n>256?b[256]:this.BMAX;p=b;pidx=0;i=n;do{c[p[pidx]]++;pidx++;}while(--i>0);if(c[0]==n){this.root=null;this.m=0;this.status=0;return;}
for(j=1;j<=this.BMAX;j++)
if(c[j]!=0)
break;k=j;if(mm<j)
mm=j;for(i=this.BMAX;i!=0;i--)
if(c[i]!=0)
break;g=i;if(mm>i)
mm=i;for(y=1<<j;j<i;j++,y<<=1)
if((y-=c[j])<0){this.status=2;this.m=mm;return;}
if((y-=c[i])<0){this.status=2;this.m=mm;return;}
c[i]+=y;x[1]=j=0;p=c;pidx=1;xp=2;while(--i>0)
x[xp++]=(j+=p[pidx++]);p=b;pidx=0;i=0;do{if((j=p[pidx++])!=0)
v[x[j]++]=i;}while(++i<n);n=x[g];x[0]=i=0;p=v;pidx=0;h=-1;w=lx[0]=0;q=null;z=0;for(;k<=g;k++){a=c[k];while(a-->0){while(k>w+lx[1+h]){w+=lx[1+h];h++;z=(z=g-w)>mm?mm:z;if((f=1<<(j=k-w))>a+1){f-=a+1;xp=k;while(++j<z){if((f<<=1)<=c[++xp])
break;f-=c[xp];}}
if(w+j>el&&w<el)
j=el-w;z=1<<j;lx[1+h]=j;q=new Array(z);for(o=0;o<z;o++){q[o]=new zip_HuftNode();}
if(tail==null)
tail=this.root=new zip_HuftList();else
tail=tail.next=new zip_HuftList();tail.next=null;tail.list=q;u[h]=q;if(h>0){x[h]=i;r.b=lx[h];r.e=16+j;r.t=q;j=(i&((1<<w)-1))>>(w-lx[h]);u[h-1][j].e=r.e;u[h-1][j].b=r.b;u[h-1][j].n=r.n;u[h-1][j].t=r.t;}}
r.b=k-w;if(pidx>=n)
r.e=99;else if(p[pidx]<s){r.e=(p[pidx]<256?16:15);r.n=p[pidx++];}else{r.e=e[p[pidx]-s];r.n=d[p[pidx++]-s];}
f=1<<(k-w);for(j=i>>w;j<z;j+=f){q[j].e=r.e;q[j].b=r.b;q[j].n=r.n;q[j].t=r.t;}
for(j=1<<(k-1);(i&j)!=0;j>>=1)
i^=j;i^=j;while((i&((1<<w)-1))!=x[h]){w-=lx[h];h--;}}}
this.m=lx[1];this.status=((y!=0&&g!=1)?1:0);}}
var zip_GET_BYTE=function(){if(zip_inflate_data.length==zip_inflate_pos)
return-1;return zip_inflate_data.charCodeAt(zip_inflate_pos++)&0xff;}
var zip_NEEDBITS=function(n){while(zip_bit_len<n){zip_bit_buf|=zip_GET_BYTE()<<zip_bit_len;zip_bit_len+=8;}}
var zip_GETBITS=function(n){return zip_bit_buf&zip_MASK_BITS[n];}
var zip_DUMPBITS=function(n){zip_bit_buf>>=n;zip_bit_len-=n;}
var zip_inflate_codes=function(buff,off,size){var e;var t;var n;if(size==0)
return 0;n=0;for(;;){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);if(e==16){zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=t.n;if(n==size)
return size;continue;}
if(e==15)
break;zip_NEEDBITS(e);zip_copy_leng=t.n+zip_GETBITS(e);zip_DUMPBITS(e);zip_NEEDBITS(zip_bd);t=zip_td.list[zip_GETBITS(zip_bd)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);zip_NEEDBITS(e);zip_copy_dist=zip_wp-t.n-zip_GETBITS(e);zip_DUMPBITS(e);while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}
if(n==size)
return size;}
zip_method=-1;return n;}
var zip_inflate_stored=function(buff,off,size){var n;n=zip_bit_len&7;zip_DUMPBITS(n);zip_NEEDBITS(16);n=zip_GETBITS(16);zip_DUMPBITS(16);zip_NEEDBITS(16);if(n!=((~zip_bit_buf)&0xffff))
return-1;zip_DUMPBITS(16);zip_copy_leng=n;n=0;while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;return n;}
var zip_inflate_fixed=function(buff,off,size){if(zip_fixed_tl==null){var i;var l=new Array(288);var h;for(i=0;i<144;i++)
l[i]=8;for(;i<256;i++)
l[i]=9;for(;i<280;i++)
l[i]=7;for(;i<288;i++)
l[i]=8;zip_fixed_bl=7;h=new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);if(h.status!=0){alert("HufBuild error: "+h.status);return-1;}
zip_fixed_tl=h.root;zip_fixed_bl=h.m;for(i=0;i<30;i++)
l[i]=5;zip_fixed_bd=5;h=new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);if(h.status>1){zip_fixed_tl=null;alert("HufBuild error: "+h.status);return-1;}
zip_fixed_td=h.root;zip_fixed_bd=h.m;}
zip_tl=zip_fixed_tl;zip_td=zip_fixed_td;zip_bl=zip_fixed_bl;zip_bd=zip_fixed_bd;return zip_inflate_codes(buff,off,size);}
var zip_inflate_dynamic=function(buff,off,size){var i;var j;var l;var n;var t;var nb;var nl;var nd;var ll=new Array(286+30);var h;for(i=0;i<ll.length;i++)
ll[i]=0;zip_NEEDBITS(5);nl=257+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(5);nd=1+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(4);nb=4+zip_GETBITS(4);zip_DUMPBITS(4);if(nl>286||nd>30)
return-1;for(j=0;j<nb;j++)
{zip_NEEDBITS(3);ll[zip_border[j]]=zip_GETBITS(3);zip_DUMPBITS(3);}
for(;j<19;j++)
ll[zip_border[j]]=0;zip_bl=7;h=new zip_HuftBuild(ll,19,19,null,null,zip_bl);if(h.status!=0)
return-1;zip_tl=h.root;zip_bl=h.m;n=nl+nd;i=l=0;while(i<n){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];j=t.b;zip_DUMPBITS(j);j=t.n;if(j<16)
ll[i++]=l=j;else if(j==16){zip_NEEDBITS(2);j=3+zip_GETBITS(2);zip_DUMPBITS(2);if(i+j>n)
return-1;while(j-->0)
ll[i++]=l;}else if(j==17){zip_NEEDBITS(3);j=3+zip_GETBITS(3);zip_DUMPBITS(3);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}else{zip_NEEDBITS(7);j=11+zip_GETBITS(7);zip_DUMPBITS(7);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}}
zip_bl=zip_lbits;h=new zip_HuftBuild(ll,nl,257,zip_cplens,zip_cplext,zip_bl);if(zip_bl==0)
h.status=1;if(h.status!=0){if(h.status==1);return-1;}
zip_tl=h.root;zip_bl=h.m;for(i=0;i<nd;i++)
ll[i]=ll[i+nl];zip_bd=zip_dbits;h=new zip_HuftBuild(ll,nd,0,zip_cpdist,zip_cpdext,zip_bd);zip_td=h.root;zip_bd=h.m;if(zip_bd==0&&nl>257){return-1;}
if(h.status==1){;}
if(h.status!=0)
return-1;return zip_inflate_codes(buff,off,size);}
var zip_inflate_start=function(){var i;if(zip_slide==null)
zip_slide=new Array(2*zip_WSIZE);zip_wp=0;zip_bit_buf=0;zip_bit_len=0;zip_method=-1;zip_eof=false;zip_copy_leng=zip_copy_dist=0;zip_tl=null;}
var zip_inflate_internal=function(buff,off,size){var n,i;n=0;while(n<size){if(zip_eof&&zip_method==-1)
return n;if(zip_copy_leng>0){if(zip_method!=zip_STORED_BLOCK){while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}}else{while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;}
if(n==size)
return n;}
if(zip_method==-1){if(zip_eof)
break;zip_NEEDBITS(1);if(zip_GETBITS(1)!=0)
zip_eof=true;zip_DUMPBITS(1);zip_NEEDBITS(2);zip_method=zip_GETBITS(2);zip_DUMPBITS(2);zip_tl=null;zip_copy_leng=0;}
switch(zip_method){case 0:i=zip_inflate_stored(buff,off+n,size-n);break;case 1:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_fixed(buff,off+n,size-n);break;case 2:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_dynamic(buff,off+n,size-n);break;default:i=-1;break;}
if(i==-1){if(zip_eof)
return 0;return-1;}
n+=i;}
return n;}
var zip_inflate=function(str){var i,j;zip_inflate_start();zip_inflate_data=str;zip_inflate_pos=0;var buff=new Array(1024);var aout=[];while((i=zip_inflate_internal(buff,0,buff.length))>0){var cbuf=new Array(i);for(j=0;j<i;j++){cbuf[j]=String.fromCharCode(buff[j]);}
aout[aout.length]=cbuf.join("");}
zip_inflate_data=null;return aout.join("");}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;})();_pybloqs_load_sentinel_jsinflate = true;}
  </script>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_block_core) == 'undefined'){function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}_pybloqs_load_sentinel_block_core = true;}
  </script>
  <style type="text/css">
   .pybloqs {
    font-family: Helvetica, "Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, sans-serif;
}

.pybloqs pre code {
    display: block;
    margin-left: 1em;
    font-family: monospace;
}
  </style>
 </head>
 <body>
  <div class="pybloqs">
   <table border="0" cellpadding="1" cellspacing="0" style="margin-left:auto; margin-right:auto; page-break-inside:avoid;">
    <thead style="display:table-header-group;">
     <tr style="page-break-inside:avoid;">
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       ABC
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       aa
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       bb
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       cc
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       dd
      </th>
     </tr>
    </thead>
    <tbody>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       a
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.36
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.77
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       b
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.62
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.56
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       c
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.11
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.75
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.37
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       d
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.34
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.71
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.95
      </td>
     </tr>
    </tbody>
   </table>
  </div>
 </body>
</html>


NB: The grid between cells is from jupyter default CSS. It will not show if the block is displayed with b.show() .

## Formatting Tables with Table Formatters
Formatters are functions which add a single specific formatting aspect (e.g. bold, font-size, alignment, multi-index display). Formatters can be stacked together as a list to produce desired layout. The list is then passed to ```HTMLJinjaTableBlock```.

Use of default formatters can be disabled completely. Additional formatters can be used on top or instead of default formatters.
Formatters change appearance by modifying cell values and adding CSS styles.

'Exotic' formatters, which are used only in a single context, can be defined locally.
A set of general use formatters can be found in pybloqs.block.table_formatters.

All formatters take the following parameters:
```
:rows List of rows, where formatter should be applied
:columns List of columns, where formatter should be applied
:apply_to_header_and_index True/False, if set to True, formatter will be applied to all index and header cells
```
If rows and columns are both ```None```, formatter is applied to all cells in table.

An example:


    import pybloqs.block.table_formatters as tf
    table_block = Block(df)
    table_block_raw = Block(df, use_default_formatters=False)
    
    fmt_pct = tf.FmtPercent(1, columns=['bb','cc'], apply_to_header_and_index=False)
    fmt_totals = tf.FmtAppendTotalsRow(total_columns=['aa','dd'])
    fmt_highlight = tf.FmtHighlightText(columns=['bb'], rows=['d'], apply_to_header_and_index=False)
    formatters=[fmt_pct,fmt_totals, fmt_highlight]
    table_block_additional_formatters = Block(df, formatters=formatters)
    
    fmt_mult = tf.FmtMultiplyCellValue(1e6, '')
    fmt_sep = tf.FmtThousandSeparator()
    formatters=[fmt_mult, fmt_sep]
    table_block_new_formatters = Block(df, formatters=formatters, use_default_formatters=False)
    
    row1 = abl.HStack([table_block, table_block_raw])
    row2 = abl.HStack([table_block_additional_formatters, table_block_new_formatters])
    all_tables = abl.VStack([row1,row2])
    
    display(HTML(all_tables.render_html()))



<!DOCTYPE html>
<html>
 <head>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_jsinflate) == 'undefined'){(function(){var zip_WSIZE=32768;var zip_STORED_BLOCK=0;var zip_STATIC_TREES=1;var zip_DYN_TREES=2;var zip_lbits=9;var zip_dbits=6;var zip_INBUFSIZ=32768;var zip_INBUF_EXTRA=64;var zip_slide;var zip_wp;var zip_fixed_tl=null;var zip_fixed_td;var zip_fixed_bl,fixed_bd;var zip_bit_buf;var zip_bit_len;var zip_method;var zip_eof;var zip_copy_leng;var zip_copy_dist;var zip_tl,zip_td;var zip_bl,zip_bd;var zip_inflate_data;var zip_inflate_pos;var zip_MASK_BITS=new Array(0x0000,0x0001,0x0003,0x0007,0x000f,0x001f,0x003f,0x007f,0x00ff,0x01ff,0x03ff,0x07ff,0x0fff,0x1fff,0x3fff,0x7fff,0xffff);var zip_cplens=new Array(3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258,0,0);var zip_cplext=new Array(0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,99,99);var zip_cpdist=new Array(1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577);var zip_cpdext=new Array(0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13);var zip_border=new Array(16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15);var zip_HuftList=function(){this.next=null;this.list=null;}
var zip_HuftNode=function(){this.e=0;this.b=0;this.n=0;this.t=null;}
var zip_HuftBuild=function(b,n,s,d,e,mm){this.BMAX=16;this.N_MAX=288;this.status=0;this.root=null;this.m=0;{var a;var c=new Array(this.BMAX+1);var el;var f;var g;var h;var i;var j;var k;var lx=new Array(this.BMAX+1);var p;var pidx;var q;var r=new zip_HuftNode();var u=new Array(this.BMAX);var v=new Array(this.N_MAX);var w;var x=new Array(this.BMAX+1);var xp;var y;var z;var o;var tail;tail=this.root=null;for(i=0;i<c.length;i++)
c[i]=0;for(i=0;i<lx.length;i++)
lx[i]=0;for(i=0;i<u.length;i++)
u[i]=null;for(i=0;i<v.length;i++)
v[i]=0;for(i=0;i<x.length;i++)
x[i]=0;el=n>256?b[256]:this.BMAX;p=b;pidx=0;i=n;do{c[p[pidx]]++;pidx++;}while(--i>0);if(c[0]==n){this.root=null;this.m=0;this.status=0;return;}
for(j=1;j<=this.BMAX;j++)
if(c[j]!=0)
break;k=j;if(mm<j)
mm=j;for(i=this.BMAX;i!=0;i--)
if(c[i]!=0)
break;g=i;if(mm>i)
mm=i;for(y=1<<j;j<i;j++,y<<=1)
if((y-=c[j])<0){this.status=2;this.m=mm;return;}
if((y-=c[i])<0){this.status=2;this.m=mm;return;}
c[i]+=y;x[1]=j=0;p=c;pidx=1;xp=2;while(--i>0)
x[xp++]=(j+=p[pidx++]);p=b;pidx=0;i=0;do{if((j=p[pidx++])!=0)
v[x[j]++]=i;}while(++i<n);n=x[g];x[0]=i=0;p=v;pidx=0;h=-1;w=lx[0]=0;q=null;z=0;for(;k<=g;k++){a=c[k];while(a-->0){while(k>w+lx[1+h]){w+=lx[1+h];h++;z=(z=g-w)>mm?mm:z;if((f=1<<(j=k-w))>a+1){f-=a+1;xp=k;while(++j<z){if((f<<=1)<=c[++xp])
break;f-=c[xp];}}
if(w+j>el&&w<el)
j=el-w;z=1<<j;lx[1+h]=j;q=new Array(z);for(o=0;o<z;o++){q[o]=new zip_HuftNode();}
if(tail==null)
tail=this.root=new zip_HuftList();else
tail=tail.next=new zip_HuftList();tail.next=null;tail.list=q;u[h]=q;if(h>0){x[h]=i;r.b=lx[h];r.e=16+j;r.t=q;j=(i&((1<<w)-1))>>(w-lx[h]);u[h-1][j].e=r.e;u[h-1][j].b=r.b;u[h-1][j].n=r.n;u[h-1][j].t=r.t;}}
r.b=k-w;if(pidx>=n)
r.e=99;else if(p[pidx]<s){r.e=(p[pidx]<256?16:15);r.n=p[pidx++];}else{r.e=e[p[pidx]-s];r.n=d[p[pidx++]-s];}
f=1<<(k-w);for(j=i>>w;j<z;j+=f){q[j].e=r.e;q[j].b=r.b;q[j].n=r.n;q[j].t=r.t;}
for(j=1<<(k-1);(i&j)!=0;j>>=1)
i^=j;i^=j;while((i&((1<<w)-1))!=x[h]){w-=lx[h];h--;}}}
this.m=lx[1];this.status=((y!=0&&g!=1)?1:0);}}
var zip_GET_BYTE=function(){if(zip_inflate_data.length==zip_inflate_pos)
return-1;return zip_inflate_data.charCodeAt(zip_inflate_pos++)&0xff;}
var zip_NEEDBITS=function(n){while(zip_bit_len<n){zip_bit_buf|=zip_GET_BYTE()<<zip_bit_len;zip_bit_len+=8;}}
var zip_GETBITS=function(n){return zip_bit_buf&zip_MASK_BITS[n];}
var zip_DUMPBITS=function(n){zip_bit_buf>>=n;zip_bit_len-=n;}
var zip_inflate_codes=function(buff,off,size){var e;var t;var n;if(size==0)
return 0;n=0;for(;;){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);if(e==16){zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=t.n;if(n==size)
return size;continue;}
if(e==15)
break;zip_NEEDBITS(e);zip_copy_leng=t.n+zip_GETBITS(e);zip_DUMPBITS(e);zip_NEEDBITS(zip_bd);t=zip_td.list[zip_GETBITS(zip_bd)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);zip_NEEDBITS(e);zip_copy_dist=zip_wp-t.n-zip_GETBITS(e);zip_DUMPBITS(e);while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}
if(n==size)
return size;}
zip_method=-1;return n;}
var zip_inflate_stored=function(buff,off,size){var n;n=zip_bit_len&7;zip_DUMPBITS(n);zip_NEEDBITS(16);n=zip_GETBITS(16);zip_DUMPBITS(16);zip_NEEDBITS(16);if(n!=((~zip_bit_buf)&0xffff))
return-1;zip_DUMPBITS(16);zip_copy_leng=n;n=0;while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;return n;}
var zip_inflate_fixed=function(buff,off,size){if(zip_fixed_tl==null){var i;var l=new Array(288);var h;for(i=0;i<144;i++)
l[i]=8;for(;i<256;i++)
l[i]=9;for(;i<280;i++)
l[i]=7;for(;i<288;i++)
l[i]=8;zip_fixed_bl=7;h=new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);if(h.status!=0){alert("HufBuild error: "+h.status);return-1;}
zip_fixed_tl=h.root;zip_fixed_bl=h.m;for(i=0;i<30;i++)
l[i]=5;zip_fixed_bd=5;h=new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);if(h.status>1){zip_fixed_tl=null;alert("HufBuild error: "+h.status);return-1;}
zip_fixed_td=h.root;zip_fixed_bd=h.m;}
zip_tl=zip_fixed_tl;zip_td=zip_fixed_td;zip_bl=zip_fixed_bl;zip_bd=zip_fixed_bd;return zip_inflate_codes(buff,off,size);}
var zip_inflate_dynamic=function(buff,off,size){var i;var j;var l;var n;var t;var nb;var nl;var nd;var ll=new Array(286+30);var h;for(i=0;i<ll.length;i++)
ll[i]=0;zip_NEEDBITS(5);nl=257+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(5);nd=1+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(4);nb=4+zip_GETBITS(4);zip_DUMPBITS(4);if(nl>286||nd>30)
return-1;for(j=0;j<nb;j++)
{zip_NEEDBITS(3);ll[zip_border[j]]=zip_GETBITS(3);zip_DUMPBITS(3);}
for(;j<19;j++)
ll[zip_border[j]]=0;zip_bl=7;h=new zip_HuftBuild(ll,19,19,null,null,zip_bl);if(h.status!=0)
return-1;zip_tl=h.root;zip_bl=h.m;n=nl+nd;i=l=0;while(i<n){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];j=t.b;zip_DUMPBITS(j);j=t.n;if(j<16)
ll[i++]=l=j;else if(j==16){zip_NEEDBITS(2);j=3+zip_GETBITS(2);zip_DUMPBITS(2);if(i+j>n)
return-1;while(j-->0)
ll[i++]=l;}else if(j==17){zip_NEEDBITS(3);j=3+zip_GETBITS(3);zip_DUMPBITS(3);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}else{zip_NEEDBITS(7);j=11+zip_GETBITS(7);zip_DUMPBITS(7);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}}
zip_bl=zip_lbits;h=new zip_HuftBuild(ll,nl,257,zip_cplens,zip_cplext,zip_bl);if(zip_bl==0)
h.status=1;if(h.status!=0){if(h.status==1);return-1;}
zip_tl=h.root;zip_bl=h.m;for(i=0;i<nd;i++)
ll[i]=ll[i+nl];zip_bd=zip_dbits;h=new zip_HuftBuild(ll,nd,0,zip_cpdist,zip_cpdext,zip_bd);zip_td=h.root;zip_bd=h.m;if(zip_bd==0&&nl>257){return-1;}
if(h.status==1){;}
if(h.status!=0)
return-1;return zip_inflate_codes(buff,off,size);}
var zip_inflate_start=function(){var i;if(zip_slide==null)
zip_slide=new Array(2*zip_WSIZE);zip_wp=0;zip_bit_buf=0;zip_bit_len=0;zip_method=-1;zip_eof=false;zip_copy_leng=zip_copy_dist=0;zip_tl=null;}
var zip_inflate_internal=function(buff,off,size){var n,i;n=0;while(n<size){if(zip_eof&&zip_method==-1)
return n;if(zip_copy_leng>0){if(zip_method!=zip_STORED_BLOCK){while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}}else{while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;}
if(n==size)
return n;}
if(zip_method==-1){if(zip_eof)
break;zip_NEEDBITS(1);if(zip_GETBITS(1)!=0)
zip_eof=true;zip_DUMPBITS(1);zip_NEEDBITS(2);zip_method=zip_GETBITS(2);zip_DUMPBITS(2);zip_tl=null;zip_copy_leng=0;}
switch(zip_method){case 0:i=zip_inflate_stored(buff,off+n,size-n);break;case 1:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_fixed(buff,off+n,size-n);break;case 2:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_dynamic(buff,off+n,size-n);break;default:i=-1;break;}
if(i==-1){if(zip_eof)
return 0;return-1;}
n+=i;}
return n;}
var zip_inflate=function(str){var i,j;zip_inflate_start();zip_inflate_data=str;zip_inflate_pos=0;var buff=new Array(1024);var aout=[];while((i=zip_inflate_internal(buff,0,buff.length))>0){var cbuf=new Array(i);for(j=0;j<i;j++){cbuf[j]=String.fromCharCode(buff[j]);}
aout[aout.length]=cbuf.join("");}
zip_inflate_data=null;return aout.join("");}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;})();_pybloqs_load_sentinel_jsinflate = true;}
  </script>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_block_core) == 'undefined'){function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}_pybloqs_load_sentinel_block_core = true;}
  </script>
  <style type="text/css">
   .pybloqs {
    font-family: Helvetica, "Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, sans-serif;
}

.pybloqs pre code {
    display: block;
    margin-left: 1em;
    font-family: monospace;
}
  </style>
 </head>
 <body>
  <div class="pybloqs">
   <div>
    <div class="pybloqs">
     <div class="pybloqs-grid-row">
      <div class="pybloqs-grid-cell" style="width:50.000000%;float:left;">
       <div class="pybloqs">
        <table border="0" cellpadding="1" cellspacing="0" style="margin-left:auto; margin-right:auto; page-break-inside:avoid;">
         <thead style="display:table-header-group;">
          <tr style="page-break-inside:avoid;">
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            ABC
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            aa
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            bb
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            cc
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            dd
           </th>
          </tr>
         </thead>
         <tbody>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            a
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.49
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.36
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.97
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.77
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
            b
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.07
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.62
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.07
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.56
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            c
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.39
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.11
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.75
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.37
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
            d
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.34
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.20
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.71
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.95
           </td>
          </tr>
         </tbody>
        </table>
       </div>
      </div>
      <div class="pybloqs-grid-cell" style="width:50.000000%;float:left;">
       <div class="pybloqs">
        <table border="0" cellpadding="1" cellspacing="0" style="">
         <thead style="">
          <tr style="">
           <th style="">
            ABC
           </th>
           <th style="">
            aa
           </th>
           <th style="">
            bb
           </th>
           <th style="">
            cc
           </th>
           <th style="">
            dd
           </th>
          </tr>
         </thead>
         <tbody>
          <tr style="">
           <td style="">
            a
           </td>
           <td style="">
            0.491425968128
           </td>
           <td style="">
            0.355021291548
           </td>
           <td style="">
            0.969661643322
           </td>
           <td style="">
            0.771977085029
           </td>
          </tr>
          <tr style="">
           <td style="">
            b
           </td>
           <td style="">
            0.066542981958
           </td>
           <td style="">
            0.622449011817
           </td>
           <td style="">
            0.0709732127762
           </td>
           <td style="">
            0.557307898499
           </td>
          </tr>
          <tr style="">
           <td style="">
            c
           </td>
           <td style="">
            0.392367746736
           </td>
           <td style="">
            0.105056261555
           </td>
           <td style="">
            0.745123712728
           </td>
           <td style="">
            0.372812760257
           </td>
          </tr>
          <tr style="">
           <td style="">
            d
           </td>
           <td style="">
            0.337316831943
           </td>
           <td style="">
            0.198479494974
           </td>
           <td style="">
            0.708809001578
           </td>
           <td style="">
            0.952886753603
           </td>
          </tr>
         </tbody>
        </table>
       </div>
      </div>
     </div>
     <div style="clear:both">
     </div>
    </div>
   </div>
   <div>
    <div class="pybloqs">
     <div class="pybloqs-grid-row">
      <div class="pybloqs-grid-cell" style="width:50.000000%;float:left;">
       <div class="pybloqs">
        <table border="0" cellpadding="1" cellspacing="0" style="margin-left:auto; margin-right:auto; page-break-inside:avoid;">
         <thead style="display:table-header-group;">
          <tr style="page-break-inside:avoid;">
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            ABC
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            aa
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            bb
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            cc
           </th>
           <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            dd
           </th>
          </tr>
         </thead>
         <tbody>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            a
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.49
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            35.5%
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            97.0%
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.77
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
            b
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.07
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            62.2%
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            7.1%
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.56
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
            c
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.39
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            10.5%
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            74.5%
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
            0.37
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
            d
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.34
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; color:rgb(52,137,188); font-weight:bold; font-style:italic;">
            19.8%
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            70.9%
           </td>
           <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
            0.95
           </td>
          </tr>
          <tr style="page-break-inside:avoid;">
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; font-weight:bold; background-color:rgb(229,229,229); border-top:1px solid rgb(30,51,124)">
            Total
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; font-weight:bold; background-color:rgb(229,229,229); border-top:1px solid rgb(30,51,124)">
            1.29
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; font-weight:bold; background-color:rgb(229,229,229); border-top:1px solid rgb(30,51,124)">
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; font-weight:bold; background-color:rgb(229,229,229); border-top:1px solid rgb(30,51,124)">
           </td>
           <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; font-weight:bold; background-color:rgb(229,229,229); border-top:1px solid rgb(30,51,124)">
            2.65
           </td>
          </tr>
         </tbody>
        </table>
       </div>
      </div>
      <div class="pybloqs-grid-cell" style="width:50.000000%;float:left;">
       <div class="pybloqs">
        <table border="0" cellpadding="1" cellspacing="0" style="">
         <thead style="">
          <tr style="">
           <th style="">
            ABC
           </th>
           <th style="">
            aa
           </th>
           <th style="">
            bb
           </th>
           <th style="">
            cc
           </th>
           <th style="">
            dd
           </th>
          </tr>
         </thead>
         <tbody>
          <tr style="">
           <td style="">
            a
           </td>
           <td style="">
            491,426
           </td>
           <td style="">
            355,021
           </td>
           <td style="">
            969,662
           </td>
           <td style="">
            771,977
           </td>
          </tr>
          <tr style="">
           <td style="">
            b
           </td>
           <td style="">
            66,543
           </td>
           <td style="">
            622,449
           </td>
           <td style="">
            70,973
           </td>
           <td style="">
            557,308
           </td>
          </tr>
          <tr style="">
           <td style="">
            c
           </td>
           <td style="">
            392,368
           </td>
           <td style="">
            105,056
           </td>
           <td style="">
            745,124
           </td>
           <td style="">
            372,813
           </td>
          </tr>
          <tr style="">
           <td style="">
            d
           </td>
           <td style="">
            337,317
           </td>
           <td style="">
            198,479
           </td>
           <td style="">
            708,809
           </td>
           <td style="">
            952,887
           </td>
          </tr>
         </tbody>
        </table>
       </div>
      </div>
     </div>
     <div style="clear:both">
     </div>
    </div>
   </div>
  </div>
 </body>
</html>


### General formatters
The following formatters handle miscalleneous general tasks
#### Replace NaN
```
FmtReplaceNaN(value='')
```
Replaces all np.nan values in specified range with provided ```value```. By default uses empty string.

#### FmtAlignCellContents
```
FmtAlignCellContents(alignment='center')
```
Aligns content inside cells within specified range. Valid values for ```alignment``` are ```left|right|center|justify|initial|inherit``` (anything that the CSS tag ```text-align``` understands).

#### FmtAlignTable
```
FmtAlignTable(alignment)
```
Aligns the entire table relative to its entironment. Valid values for alignment are ```center```, ```right```, ```left```.

#### FmtHeader
```
FmtHeader(fixed_width='100%', index_width=None, column_width=None, rotate_deg=0,top_padding=None, no_wrap=True)
```
Creates a table with fixed-width columns. 
```
:fixed_width Total width of table
:index_width Fixed width of index column
:column_width Fixed width of all other columns
:rotate_deg Value in degrees by which to rotate table header cells
:top_padding: additional vertical space above table, may be necessary when using rotated headers
:no_wrap True/False, disables line-breaks within header cell when set to True
```
An example (NB, jypiter ignores top-padding, which otherwise works in direkt browser display and PDF output):


    fmt_header = tf.FmtHeader(fixed_width='20cm',index_width='30%', top_padding='3cm', rotate_deg=30)
    table_block = Block(df, formatters=[fmt_header])
    display(HTML(table_block.render_html()))


<!DOCTYPE html>
<html>
 <head>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_jsinflate) == 'undefined'){(function(){var zip_WSIZE=32768;var zip_STORED_BLOCK=0;var zip_STATIC_TREES=1;var zip_DYN_TREES=2;var zip_lbits=9;var zip_dbits=6;var zip_INBUFSIZ=32768;var zip_INBUF_EXTRA=64;var zip_slide;var zip_wp;var zip_fixed_tl=null;var zip_fixed_td;var zip_fixed_bl,fixed_bd;var zip_bit_buf;var zip_bit_len;var zip_method;var zip_eof;var zip_copy_leng;var zip_copy_dist;var zip_tl,zip_td;var zip_bl,zip_bd;var zip_inflate_data;var zip_inflate_pos;var zip_MASK_BITS=new Array(0x0000,0x0001,0x0003,0x0007,0x000f,0x001f,0x003f,0x007f,0x00ff,0x01ff,0x03ff,0x07ff,0x0fff,0x1fff,0x3fff,0x7fff,0xffff);var zip_cplens=new Array(3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258,0,0);var zip_cplext=new Array(0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,99,99);var zip_cpdist=new Array(1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577);var zip_cpdext=new Array(0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13);var zip_border=new Array(16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15);var zip_HuftList=function(){this.next=null;this.list=null;}
var zip_HuftNode=function(){this.e=0;this.b=0;this.n=0;this.t=null;}
var zip_HuftBuild=function(b,n,s,d,e,mm){this.BMAX=16;this.N_MAX=288;this.status=0;this.root=null;this.m=0;{var a;var c=new Array(this.BMAX+1);var el;var f;var g;var h;var i;var j;var k;var lx=new Array(this.BMAX+1);var p;var pidx;var q;var r=new zip_HuftNode();var u=new Array(this.BMAX);var v=new Array(this.N_MAX);var w;var x=new Array(this.BMAX+1);var xp;var y;var z;var o;var tail;tail=this.root=null;for(i=0;i<c.length;i++)
c[i]=0;for(i=0;i<lx.length;i++)
lx[i]=0;for(i=0;i<u.length;i++)
u[i]=null;for(i=0;i<v.length;i++)
v[i]=0;for(i=0;i<x.length;i++)
x[i]=0;el=n>256?b[256]:this.BMAX;p=b;pidx=0;i=n;do{c[p[pidx]]++;pidx++;}while(--i>0);if(c[0]==n){this.root=null;this.m=0;this.status=0;return;}
for(j=1;j<=this.BMAX;j++)
if(c[j]!=0)
break;k=j;if(mm<j)
mm=j;for(i=this.BMAX;i!=0;i--)
if(c[i]!=0)
break;g=i;if(mm>i)
mm=i;for(y=1<<j;j<i;j++,y<<=1)
if((y-=c[j])<0){this.status=2;this.m=mm;return;}
if((y-=c[i])<0){this.status=2;this.m=mm;return;}
c[i]+=y;x[1]=j=0;p=c;pidx=1;xp=2;while(--i>0)
x[xp++]=(j+=p[pidx++]);p=b;pidx=0;i=0;do{if((j=p[pidx++])!=0)
v[x[j]++]=i;}while(++i<n);n=x[g];x[0]=i=0;p=v;pidx=0;h=-1;w=lx[0]=0;q=null;z=0;for(;k<=g;k++){a=c[k];while(a-->0){while(k>w+lx[1+h]){w+=lx[1+h];h++;z=(z=g-w)>mm?mm:z;if((f=1<<(j=k-w))>a+1){f-=a+1;xp=k;while(++j<z){if((f<<=1)<=c[++xp])
break;f-=c[xp];}}
if(w+j>el&&w<el)
j=el-w;z=1<<j;lx[1+h]=j;q=new Array(z);for(o=0;o<z;o++){q[o]=new zip_HuftNode();}
if(tail==null)
tail=this.root=new zip_HuftList();else
tail=tail.next=new zip_HuftList();tail.next=null;tail.list=q;u[h]=q;if(h>0){x[h]=i;r.b=lx[h];r.e=16+j;r.t=q;j=(i&((1<<w)-1))>>(w-lx[h]);u[h-1][j].e=r.e;u[h-1][j].b=r.b;u[h-1][j].n=r.n;u[h-1][j].t=r.t;}}
r.b=k-w;if(pidx>=n)
r.e=99;else if(p[pidx]<s){r.e=(p[pidx]<256?16:15);r.n=p[pidx++];}else{r.e=e[p[pidx]-s];r.n=d[p[pidx++]-s];}
f=1<<(k-w);for(j=i>>w;j<z;j+=f){q[j].e=r.e;q[j].b=r.b;q[j].n=r.n;q[j].t=r.t;}
for(j=1<<(k-1);(i&j)!=0;j>>=1)
i^=j;i^=j;while((i&((1<<w)-1))!=x[h]){w-=lx[h];h--;}}}
this.m=lx[1];this.status=((y!=0&&g!=1)?1:0);}}
var zip_GET_BYTE=function(){if(zip_inflate_data.length==zip_inflate_pos)
return-1;return zip_inflate_data.charCodeAt(zip_inflate_pos++)&0xff;}
var zip_NEEDBITS=function(n){while(zip_bit_len<n){zip_bit_buf|=zip_GET_BYTE()<<zip_bit_len;zip_bit_len+=8;}}
var zip_GETBITS=function(n){return zip_bit_buf&zip_MASK_BITS[n];}
var zip_DUMPBITS=function(n){zip_bit_buf>>=n;zip_bit_len-=n;}
var zip_inflate_codes=function(buff,off,size){var e;var t;var n;if(size==0)
return 0;n=0;for(;;){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);if(e==16){zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=t.n;if(n==size)
return size;continue;}
if(e==15)
break;zip_NEEDBITS(e);zip_copy_leng=t.n+zip_GETBITS(e);zip_DUMPBITS(e);zip_NEEDBITS(zip_bd);t=zip_td.list[zip_GETBITS(zip_bd)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);zip_NEEDBITS(e);zip_copy_dist=zip_wp-t.n-zip_GETBITS(e);zip_DUMPBITS(e);while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}
if(n==size)
return size;}
zip_method=-1;return n;}
var zip_inflate_stored=function(buff,off,size){var n;n=zip_bit_len&7;zip_DUMPBITS(n);zip_NEEDBITS(16);n=zip_GETBITS(16);zip_DUMPBITS(16);zip_NEEDBITS(16);if(n!=((~zip_bit_buf)&0xffff))
return-1;zip_DUMPBITS(16);zip_copy_leng=n;n=0;while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;return n;}
var zip_inflate_fixed=function(buff,off,size){if(zip_fixed_tl==null){var i;var l=new Array(288);var h;for(i=0;i<144;i++)
l[i]=8;for(;i<256;i++)
l[i]=9;for(;i<280;i++)
l[i]=7;for(;i<288;i++)
l[i]=8;zip_fixed_bl=7;h=new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);if(h.status!=0){alert("HufBuild error: "+h.status);return-1;}
zip_fixed_tl=h.root;zip_fixed_bl=h.m;for(i=0;i<30;i++)
l[i]=5;zip_fixed_bd=5;h=new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);if(h.status>1){zip_fixed_tl=null;alert("HufBuild error: "+h.status);return-1;}
zip_fixed_td=h.root;zip_fixed_bd=h.m;}
zip_tl=zip_fixed_tl;zip_td=zip_fixed_td;zip_bl=zip_fixed_bl;zip_bd=zip_fixed_bd;return zip_inflate_codes(buff,off,size);}
var zip_inflate_dynamic=function(buff,off,size){var i;var j;var l;var n;var t;var nb;var nl;var nd;var ll=new Array(286+30);var h;for(i=0;i<ll.length;i++)
ll[i]=0;zip_NEEDBITS(5);nl=257+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(5);nd=1+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(4);nb=4+zip_GETBITS(4);zip_DUMPBITS(4);if(nl>286||nd>30)
return-1;for(j=0;j<nb;j++)
{zip_NEEDBITS(3);ll[zip_border[j]]=zip_GETBITS(3);zip_DUMPBITS(3);}
for(;j<19;j++)
ll[zip_border[j]]=0;zip_bl=7;h=new zip_HuftBuild(ll,19,19,null,null,zip_bl);if(h.status!=0)
return-1;zip_tl=h.root;zip_bl=h.m;n=nl+nd;i=l=0;while(i<n){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];j=t.b;zip_DUMPBITS(j);j=t.n;if(j<16)
ll[i++]=l=j;else if(j==16){zip_NEEDBITS(2);j=3+zip_GETBITS(2);zip_DUMPBITS(2);if(i+j>n)
return-1;while(j-->0)
ll[i++]=l;}else if(j==17){zip_NEEDBITS(3);j=3+zip_GETBITS(3);zip_DUMPBITS(3);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}else{zip_NEEDBITS(7);j=11+zip_GETBITS(7);zip_DUMPBITS(7);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}}
zip_bl=zip_lbits;h=new zip_HuftBuild(ll,nl,257,zip_cplens,zip_cplext,zip_bl);if(zip_bl==0)
h.status=1;if(h.status!=0){if(h.status==1);return-1;}
zip_tl=h.root;zip_bl=h.m;for(i=0;i<nd;i++)
ll[i]=ll[i+nl];zip_bd=zip_dbits;h=new zip_HuftBuild(ll,nd,0,zip_cpdist,zip_cpdext,zip_bd);zip_td=h.root;zip_bd=h.m;if(zip_bd==0&&nl>257){return-1;}
if(h.status==1){;}
if(h.status!=0)
return-1;return zip_inflate_codes(buff,off,size);}
var zip_inflate_start=function(){var i;if(zip_slide==null)
zip_slide=new Array(2*zip_WSIZE);zip_wp=0;zip_bit_buf=0;zip_bit_len=0;zip_method=-1;zip_eof=false;zip_copy_leng=zip_copy_dist=0;zip_tl=null;}
var zip_inflate_internal=function(buff,off,size){var n,i;n=0;while(n<size){if(zip_eof&&zip_method==-1)
return n;if(zip_copy_leng>0){if(zip_method!=zip_STORED_BLOCK){while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}}else{while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;}
if(n==size)
return n;}
if(zip_method==-1){if(zip_eof)
break;zip_NEEDBITS(1);if(zip_GETBITS(1)!=0)
zip_eof=true;zip_DUMPBITS(1);zip_NEEDBITS(2);zip_method=zip_GETBITS(2);zip_DUMPBITS(2);zip_tl=null;zip_copy_leng=0;}
switch(zip_method){case 0:i=zip_inflate_stored(buff,off+n,size-n);break;case 1:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_fixed(buff,off+n,size-n);break;case 2:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_dynamic(buff,off+n,size-n);break;default:i=-1;break;}
if(i==-1){if(zip_eof)
return 0;return-1;}
n+=i;}
return n;}
var zip_inflate=function(str){var i,j;zip_inflate_start();zip_inflate_data=str;zip_inflate_pos=0;var buff=new Array(1024);var aout=[];while((i=zip_inflate_internal(buff,0,buff.length))>0){var cbuf=new Array(i);for(j=0;j<i;j++){cbuf[j]=String.fromCharCode(buff[j]);}
aout[aout.length]=cbuf.join("");}
zip_inflate_data=null;return aout.join("");}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;})();_pybloqs_load_sentinel_jsinflate = true;}
  </script>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_block_core) == 'undefined'){function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}_pybloqs_load_sentinel_block_core = true;}
  </script>
  <style type="text/css">
   .pybloqs {
    font-family: Helvetica, "Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, sans-serif;
}

.pybloqs pre code {
    display: block;
    margin-left: 1em;
    font-family: monospace;
}
  </style>
 </head>
 <body>
  <div class="pybloqs">
   <table border="0" cellpadding="1" cellspacing="0" style="margin-left:auto; margin-right:auto; page-break-inside:avoid;; padding-top:3cm; width:20cm; table-layout:fixed;">
    <thead style="display:table-header-group;">
     <tr style="page-break-inside:avoid;">
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; -webkit-transform-origin:0% 100%; -webkit-transform:translate(80%, 0%) rotate(-30deg); transform-origin:0% 100%; transform:translate(80%, 0%) rotate(-30deg); white-space:nowrap; width:30%">
       ABC
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; -webkit-transform-origin:0% 100%; -webkit-transform:translate(80%, 0%) rotate(-30deg); transform-origin:0% 100%; transform:translate(80%, 0%) rotate(-30deg); white-space:nowrap">
       aa
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; -webkit-transform-origin:0% 100%; -webkit-transform:translate(80%, 0%) rotate(-30deg); transform-origin:0% 100%; transform:translate(80%, 0%) rotate(-30deg); white-space:nowrap">
       bb
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; -webkit-transform-origin:0% 100%; -webkit-transform:translate(80%, 0%) rotate(-30deg); transform-origin:0% 100%; transform:translate(80%, 0%) rotate(-30deg); white-space:nowrap">
       cc
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold; -webkit-transform-origin:0% 100%; -webkit-transform:translate(80%, 0%) rotate(-30deg); transform-origin:0% 100%; transform:translate(80%, 0%) rotate(-30deg); white-space:nowrap">
       dd
      </th>
     </tr>
    </thead>
    <tbody>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       a
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.36
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.77
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       b
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.62
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.56
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       c
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.11
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.75
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.37
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       d
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.34
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.71
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.95
      </td>
     </tr>
    </tbody>
   </table>
  </div>
 </body>
</html>


#### FmtStripeBackground
```
FmtStripeBackground(first_color=colors.LIGHT_GREY, second_color=colors.WHITE, header_color=colors.WHITE,
```
Creates a repeating color patters in the background of the specified cells.
```
:first_color CSS color, for odd row numbers
:second_color CSS color, for even row numbers
:header_color CSS color applied to header row
```
#### FmtAddCellPadding
```
FmtAddCellPadding(left=None, right=None, top=None, bottom=None, length_unit='px')
```
Add space on sides of selected cells.
#### FmtAppendTotalsRow
```
FmtAppendTotalsRow(row_name='Total', operator=OP_SUM, bold=True, background_color=colors.LIGHT_GREY, font_color=None, total_columns=None)
```
Adds a line at the end of the table filled with values computed columnwise. For an example, see section [Formatting Tables with Table Formatters]
```
:row_name Label for additional row shown in index
:operator Computational operation to perform on columns, e.g. tf.OP_SUM, tf.OP_MEAN, tf.OP_NONE
:total_columns Names of columns to apply operator to. If None, operator is applied to all columns.
:bold True/False, applied bold font-style to cells in added row
:font_color CSS color for cell text in added row
:background_color CSS color for cell background in added row
```
#### FmtHideRows
```
FmtHideCells(rows=None, columns=None)
```
Hides cells in the intersection of rows and columns list. If only rows or columns is specified and the other is left None, the entire row or column is hidden.
#### FmtPageBreak
```
FmtPageBreak(no_break=True, repeat_header=True)
```
Defines table behaviour around page-breaks. Please note that Webkit-based browsers (Chrome, Safari and wkhtmltopdf as well) do not handle the ```repeat-header``` property properly, especially when headers are rotated. This bug is reported and not resolved since 6 years. Functionality in Firefox is fine, including rotated headers.
```
:no_break True/False, avoids splitting table on page break
:repeat_header True/False, when table is split accross page, repeat header on the next page
```

### Displaying text
The following formatters modify the display of both text and numbers.
#### FmtFontsize
```
FmtFontsize(fontsize, format='px')
```
Sets the font-size property of specified cells. A nice property is ```vw```, which gives the font-size as percent of viewport-width. This will scale the font with the witdh of the page and is thus suited for wide tables which should still look fine (but small) when output as PDF.

#### FmtHighlightText
```
FmtHighlightText(bold=True, italic=True, font_color=colors.BLUE)
```
Sets various properties of character display.
```
:bold True/False, sets bold font-style
:italic True/False, sets italic font-style
:font_color CSS color, sets text color
```
#### FmtHighlightBackground
```
FmtHighlightBackground(color=colors.RED)
```
Sets the background color of specified cells.

#### FmtBold
```
FmtBold()
```
Sets font-style bold in specified cells.

### Displaying numbers
The following formatters only apply to numbers. Please note that some convert the number to a string when applied.

#### FmtNumbers, FmtDecimals, FmtThousandSeparator, FmtPercent
E.g.
```
FmtPercent(n_decimals)
```
If cell content is a number, it is changed to a string with approriate formatting, e.g. number of decimals (FmtDecimals), with a comma as thousands separator (FmtThousandSeparator), or as percent with a trailing '%' sign(FmtPercent).
```
FmtNumbers(fmt_string)
```
is the general purpose formatting class, which accets any formatting string. For more information about formatting strings, see https://pyformat.info/

#### FmtMultiplyCellValue, FmtValueToMillion, FmtValueToPercent, FmtValueToBps
E.g.
```
FmtValueToPercent(suffix='%')
```
Multiplies number in cell by a given factor, thus keeping is a number. A suffix an be added to the columns header. This is useful for tables, which all contain percentage values and where a '%' sign after each value is undesireable.
```
FmtMultiplyCellValue(d, suffix)
```
is the general purpose function, multiplying by any given factor.

### Heatmaps
The table formatting has a very flexible heatmap formatter.
#### FmtHeatmap
```
FmtHeatmap(min_color=colors.HEATMAP_RED, max_color=colors.HEATMAP_GREEN, threshold=0.,axis=None)
```
Creates a heatmap in the intersection of specified columns and rows.
```
:min_color CSS color, which is the color applied as background-color at the minimum negative value
:max_color CSS color, which is the color applied as background-color at the maximum positive value
:threshold specifies an interval around 0, in which no heatmapping is applied
:axis Number, either 0 (horizontal), or 1 (vertical) or None. If None, heatmap is applied over all selected cells. If set to a number, heatmap is applied column-wise or row-wise reprectively.
```


    import string
    # Create DataFrame
    df_size = 15
    index = [c for c in string.ascii_lowercase[:df_size]]
    columns = [c+c for c in string.ascii_lowercase[:df_size]]
    df = pd.DataFrame(np.random.rand(df_size,df_size), index=index, columns=columns)
    
    # Specify heatmap formatters
    # All values in range
    fmt_heatmap1 = tf.FmtHeatmap(rows=index[10:16],columns=columns[:5])
    # By row
    fmt_heatmap2 = tf.FmtHeatmap(rows=index[:3], axis=0, max_color=(255,0,255))
    # By column
    fmt_heatmap3 = tf.FmtHeatmap(rows=index[5:],columns=columns[10:], axis=1, max_color=(255,255,0))
    
    formatters =[fmt_heatmap1, fmt_heatmap2, fmt_heatmap3]
    
    # Display
    table_block = Block(df, formatters=formatters)
    display(HTML(table_block.render_html()))


<!DOCTYPE html>
<html>
 <head>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_jsinflate) == 'undefined'){(function(){var zip_WSIZE=32768;var zip_STORED_BLOCK=0;var zip_STATIC_TREES=1;var zip_DYN_TREES=2;var zip_lbits=9;var zip_dbits=6;var zip_INBUFSIZ=32768;var zip_INBUF_EXTRA=64;var zip_slide;var zip_wp;var zip_fixed_tl=null;var zip_fixed_td;var zip_fixed_bl,fixed_bd;var zip_bit_buf;var zip_bit_len;var zip_method;var zip_eof;var zip_copy_leng;var zip_copy_dist;var zip_tl,zip_td;var zip_bl,zip_bd;var zip_inflate_data;var zip_inflate_pos;var zip_MASK_BITS=new Array(0x0000,0x0001,0x0003,0x0007,0x000f,0x001f,0x003f,0x007f,0x00ff,0x01ff,0x03ff,0x07ff,0x0fff,0x1fff,0x3fff,0x7fff,0xffff);var zip_cplens=new Array(3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258,0,0);var zip_cplext=new Array(0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,99,99);var zip_cpdist=new Array(1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577);var zip_cpdext=new Array(0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13);var zip_border=new Array(16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15);var zip_HuftList=function(){this.next=null;this.list=null;}
var zip_HuftNode=function(){this.e=0;this.b=0;this.n=0;this.t=null;}
var zip_HuftBuild=function(b,n,s,d,e,mm){this.BMAX=16;this.N_MAX=288;this.status=0;this.root=null;this.m=0;{var a;var c=new Array(this.BMAX+1);var el;var f;var g;var h;var i;var j;var k;var lx=new Array(this.BMAX+1);var p;var pidx;var q;var r=new zip_HuftNode();var u=new Array(this.BMAX);var v=new Array(this.N_MAX);var w;var x=new Array(this.BMAX+1);var xp;var y;var z;var o;var tail;tail=this.root=null;for(i=0;i<c.length;i++)
c[i]=0;for(i=0;i<lx.length;i++)
lx[i]=0;for(i=0;i<u.length;i++)
u[i]=null;for(i=0;i<v.length;i++)
v[i]=0;for(i=0;i<x.length;i++)
x[i]=0;el=n>256?b[256]:this.BMAX;p=b;pidx=0;i=n;do{c[p[pidx]]++;pidx++;}while(--i>0);if(c[0]==n){this.root=null;this.m=0;this.status=0;return;}
for(j=1;j<=this.BMAX;j++)
if(c[j]!=0)
break;k=j;if(mm<j)
mm=j;for(i=this.BMAX;i!=0;i--)
if(c[i]!=0)
break;g=i;if(mm>i)
mm=i;for(y=1<<j;j<i;j++,y<<=1)
if((y-=c[j])<0){this.status=2;this.m=mm;return;}
if((y-=c[i])<0){this.status=2;this.m=mm;return;}
c[i]+=y;x[1]=j=0;p=c;pidx=1;xp=2;while(--i>0)
x[xp++]=(j+=p[pidx++]);p=b;pidx=0;i=0;do{if((j=p[pidx++])!=0)
v[x[j]++]=i;}while(++i<n);n=x[g];x[0]=i=0;p=v;pidx=0;h=-1;w=lx[0]=0;q=null;z=0;for(;k<=g;k++){a=c[k];while(a-->0){while(k>w+lx[1+h]){w+=lx[1+h];h++;z=(z=g-w)>mm?mm:z;if((f=1<<(j=k-w))>a+1){f-=a+1;xp=k;while(++j<z){if((f<<=1)<=c[++xp])
break;f-=c[xp];}}
if(w+j>el&&w<el)
j=el-w;z=1<<j;lx[1+h]=j;q=new Array(z);for(o=0;o<z;o++){q[o]=new zip_HuftNode();}
if(tail==null)
tail=this.root=new zip_HuftList();else
tail=tail.next=new zip_HuftList();tail.next=null;tail.list=q;u[h]=q;if(h>0){x[h]=i;r.b=lx[h];r.e=16+j;r.t=q;j=(i&((1<<w)-1))>>(w-lx[h]);u[h-1][j].e=r.e;u[h-1][j].b=r.b;u[h-1][j].n=r.n;u[h-1][j].t=r.t;}}
r.b=k-w;if(pidx>=n)
r.e=99;else if(p[pidx]<s){r.e=(p[pidx]<256?16:15);r.n=p[pidx++];}else{r.e=e[p[pidx]-s];r.n=d[p[pidx++]-s];}
f=1<<(k-w);for(j=i>>w;j<z;j+=f){q[j].e=r.e;q[j].b=r.b;q[j].n=r.n;q[j].t=r.t;}
for(j=1<<(k-1);(i&j)!=0;j>>=1)
i^=j;i^=j;while((i&((1<<w)-1))!=x[h]){w-=lx[h];h--;}}}
this.m=lx[1];this.status=((y!=0&&g!=1)?1:0);}}
var zip_GET_BYTE=function(){if(zip_inflate_data.length==zip_inflate_pos)
return-1;return zip_inflate_data.charCodeAt(zip_inflate_pos++)&0xff;}
var zip_NEEDBITS=function(n){while(zip_bit_len<n){zip_bit_buf|=zip_GET_BYTE()<<zip_bit_len;zip_bit_len+=8;}}
var zip_GETBITS=function(n){return zip_bit_buf&zip_MASK_BITS[n];}
var zip_DUMPBITS=function(n){zip_bit_buf>>=n;zip_bit_len-=n;}
var zip_inflate_codes=function(buff,off,size){var e;var t;var n;if(size==0)
return 0;n=0;for(;;){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);if(e==16){zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=t.n;if(n==size)
return size;continue;}
if(e==15)
break;zip_NEEDBITS(e);zip_copy_leng=t.n+zip_GETBITS(e);zip_DUMPBITS(e);zip_NEEDBITS(zip_bd);t=zip_td.list[zip_GETBITS(zip_bd)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);zip_NEEDBITS(e);zip_copy_dist=zip_wp-t.n-zip_GETBITS(e);zip_DUMPBITS(e);while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}
if(n==size)
return size;}
zip_method=-1;return n;}
var zip_inflate_stored=function(buff,off,size){var n;n=zip_bit_len&7;zip_DUMPBITS(n);zip_NEEDBITS(16);n=zip_GETBITS(16);zip_DUMPBITS(16);zip_NEEDBITS(16);if(n!=((~zip_bit_buf)&0xffff))
return-1;zip_DUMPBITS(16);zip_copy_leng=n;n=0;while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;return n;}
var zip_inflate_fixed=function(buff,off,size){if(zip_fixed_tl==null){var i;var l=new Array(288);var h;for(i=0;i<144;i++)
l[i]=8;for(;i<256;i++)
l[i]=9;for(;i<280;i++)
l[i]=7;for(;i<288;i++)
l[i]=8;zip_fixed_bl=7;h=new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);if(h.status!=0){alert("HufBuild error: "+h.status);return-1;}
zip_fixed_tl=h.root;zip_fixed_bl=h.m;for(i=0;i<30;i++)
l[i]=5;zip_fixed_bd=5;h=new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);if(h.status>1){zip_fixed_tl=null;alert("HufBuild error: "+h.status);return-1;}
zip_fixed_td=h.root;zip_fixed_bd=h.m;}
zip_tl=zip_fixed_tl;zip_td=zip_fixed_td;zip_bl=zip_fixed_bl;zip_bd=zip_fixed_bd;return zip_inflate_codes(buff,off,size);}
var zip_inflate_dynamic=function(buff,off,size){var i;var j;var l;var n;var t;var nb;var nl;var nd;var ll=new Array(286+30);var h;for(i=0;i<ll.length;i++)
ll[i]=0;zip_NEEDBITS(5);nl=257+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(5);nd=1+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(4);nb=4+zip_GETBITS(4);zip_DUMPBITS(4);if(nl>286||nd>30)
return-1;for(j=0;j<nb;j++)
{zip_NEEDBITS(3);ll[zip_border[j]]=zip_GETBITS(3);zip_DUMPBITS(3);}
for(;j<19;j++)
ll[zip_border[j]]=0;zip_bl=7;h=new zip_HuftBuild(ll,19,19,null,null,zip_bl);if(h.status!=0)
return-1;zip_tl=h.root;zip_bl=h.m;n=nl+nd;i=l=0;while(i<n){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];j=t.b;zip_DUMPBITS(j);j=t.n;if(j<16)
ll[i++]=l=j;else if(j==16){zip_NEEDBITS(2);j=3+zip_GETBITS(2);zip_DUMPBITS(2);if(i+j>n)
return-1;while(j-->0)
ll[i++]=l;}else if(j==17){zip_NEEDBITS(3);j=3+zip_GETBITS(3);zip_DUMPBITS(3);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}else{zip_NEEDBITS(7);j=11+zip_GETBITS(7);zip_DUMPBITS(7);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}}
zip_bl=zip_lbits;h=new zip_HuftBuild(ll,nl,257,zip_cplens,zip_cplext,zip_bl);if(zip_bl==0)
h.status=1;if(h.status!=0){if(h.status==1);return-1;}
zip_tl=h.root;zip_bl=h.m;for(i=0;i<nd;i++)
ll[i]=ll[i+nl];zip_bd=zip_dbits;h=new zip_HuftBuild(ll,nd,0,zip_cpdist,zip_cpdext,zip_bd);zip_td=h.root;zip_bd=h.m;if(zip_bd==0&&nl>257){return-1;}
if(h.status==1){;}
if(h.status!=0)
return-1;return zip_inflate_codes(buff,off,size);}
var zip_inflate_start=function(){var i;if(zip_slide==null)
zip_slide=new Array(2*zip_WSIZE);zip_wp=0;zip_bit_buf=0;zip_bit_len=0;zip_method=-1;zip_eof=false;zip_copy_leng=zip_copy_dist=0;zip_tl=null;}
var zip_inflate_internal=function(buff,off,size){var n,i;n=0;while(n<size){if(zip_eof&&zip_method==-1)
return n;if(zip_copy_leng>0){if(zip_method!=zip_STORED_BLOCK){while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}}else{while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;}
if(n==size)
return n;}
if(zip_method==-1){if(zip_eof)
break;zip_NEEDBITS(1);if(zip_GETBITS(1)!=0)
zip_eof=true;zip_DUMPBITS(1);zip_NEEDBITS(2);zip_method=zip_GETBITS(2);zip_DUMPBITS(2);zip_tl=null;zip_copy_leng=0;}
switch(zip_method){case 0:i=zip_inflate_stored(buff,off+n,size-n);break;case 1:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_fixed(buff,off+n,size-n);break;case 2:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_dynamic(buff,off+n,size-n);break;default:i=-1;break;}
if(i==-1){if(zip_eof)
return 0;return-1;}
n+=i;}
return n;}
var zip_inflate=function(str){var i,j;zip_inflate_start();zip_inflate_data=str;zip_inflate_pos=0;var buff=new Array(1024);var aout=[];while((i=zip_inflate_internal(buff,0,buff.length))>0){var cbuf=new Array(i);for(j=0;j<i;j++){cbuf[j]=String.fromCharCode(buff[j]);}
aout[aout.length]=cbuf.join("");}
zip_inflate_data=null;return aout.join("");}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;})();_pybloqs_load_sentinel_jsinflate = true;}
  </script>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_block_core) == 'undefined'){function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}_pybloqs_load_sentinel_block_core = true;}
  </script>
  <style type="text/css">
   .pybloqs {
    font-family: Helvetica, "Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, sans-serif;
}

.pybloqs pre code {
    display: block;
    margin-left: 1em;
    font-family: monospace;
}
  </style>
 </head>
 <body>
  <div class="pybloqs">
   <table border="0" cellpadding="1" cellspacing="0" style="margin-left:auto; margin-right:auto; page-break-inside:avoid;">
    <thead style="display:table-header-group;">
     <tr style="page-break-inside:avoid;">
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       aa
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       bb
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       cc
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       dd
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       ee
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       ff
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       gg
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       hh
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       ii
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       jj
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       kk
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       ll
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       mm
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       nn
      </th>
      <th style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       oo
      </th>
     </tr>
    </thead>
    <tbody>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       a
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(9313,219,9313)">
       0.14
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(38211,105,38211)">
       0.58
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(50806,55,50806)">
       0.77
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(31963,130,31963)">
       0.48
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(7322,227,7322)">
       0.11
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(35837,114,35837)">
       0.54
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(9087,220,9087)">
       0.13
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(3540,242,3540)">
       0.05
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(56143,34,56143)">
       0.85
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(43510,84,43510)">
       0.66
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(25943,153,25943)">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(65025,0,65025)">
       0.99
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(58632,25,58632)">
       0.89
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(47462,69,47462)">
       0.72
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(35021,118,35021)">
       0.53
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       b
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(48877,63,48877)">
       0.74
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(64218,3,64218)">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(12488,206,12488)">
       0.19
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(65025,0,65025)">
       0.99
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(59891,20,59891)">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(6736,229,6736)">
       0.10
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(10884,213,10884)">
       0.16
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(3964,240,3964)">
       0.06
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(32485,128,32485)">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(51823,51,51823)">
       0.78
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(60942,16,60942)">
       0.92
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(52718,48,52718)">
       0.80
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(27178,149,27178)">
       0.41
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(64424,2,64424)">
       0.98
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(25173,156,25173)">
       0.38
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       c
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(4756,237,4756)">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(9554,218,9554)">
       0.14
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(28428,144,28428)">
       0.42
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(24506,159,24506)">
       0.36
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(61179,15,61179)">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(65025,0,65025)">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(5298,235,5298)">
       0.08
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(1616,249,1616)">
       0.02
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(20672,174,20672)">
       0.31
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(50668,56,50668)">
       0.75
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(41647,92,41647)">
       0.62
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(39525,100,39525)">
       0.59
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(64918,0,64918)">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(16599,190,16599)">
       0.24
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(2250,247,2250)">
       0.03
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       d
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.55
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.45
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.27
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.29
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.22
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.06
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.25
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.98
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.93
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.26
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.85
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.52
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.84
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       e
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.40
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.41
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.65
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.54
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.32
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       1.00
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.29
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.59
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.72
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.01
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.94
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.33
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.41
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       f
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.02
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.29
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.64
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.75
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.60
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.48
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.76
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.64
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.13
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(65025,65025,0)">
       0.95
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(65025,65025,0)">
       0.95
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(64221,64221,3)">
       0.94
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(45327,45327,77)">
       0.63
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(37871,37871,106)">
       0.44
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       g
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.27
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.53
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.69
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.90
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.66
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.32
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.04
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.30
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.59
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(7117,7117,227)">
       0.10
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(54826,54826,40)">
       0.80
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(23518,23518,163)">
       0.34
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(19458,19458,179)">
       0.27
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(5410,5410,234)">
       0.06
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       h
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.02
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.72
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.76
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.40
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.90
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.99
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.58
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.54
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(62290,62290,10)">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(59902,59902,20)">
       0.88
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(65025,65025,0)">
       0.95
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(60571,60571,17)">
       0.85
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(58597,58597,25)">
       0.69
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       i
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.00
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.93
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.67
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.17
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.73
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.65
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.50
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.51
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.44
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(49861,49861,59)">
       0.73
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(41818,41818,91)">
       0.61
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(38456,38456,104)">
       0.56
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(47189,47189,70)">
       0.66
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(37064,37064,110)">
       0.44
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       j
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.06
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.26
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.07
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.72
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.51
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.55
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.92
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.55
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.55
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(44845,44845,79)">
       0.65
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(29316,29316,140)">
       0.43
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(3841,3841,240)">
       0.05
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(27404,27404,148)">
       0.38
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(54025,54025,43)">
       0.64
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       k
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(152,234,152)">
       0.68
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(224,248,224)">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(223,248,223)">
       0.21
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(223,248,223)">
       0.21
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(221,248,221)">
       0.22
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.10
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.48
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.97
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.21
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.12
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(51456,51456,53)">
       0.75
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(5500,5500,234)">
       0.08
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(288,288,254)">
       0.00
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(56673,56673,32)">
       0.79
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(17003,17003,189)">
       0.20
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       l
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(178,239,178)">
       0.51
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(179,239,179)">
       0.50
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(198,243,198)">
       0.37
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(227,249,227)">
       0.18
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(210,246,210)">
       0.29
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.08
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.31
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.13
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.12
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.56
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(6358,6358,230)">
       0.09
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(33576,33576,123)">
       0.49
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(24423,24423,159)">
       0.35
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(16675,16675,190)">
       0.23
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(22671,22671,166)">
       0.27
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       m
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(192,242,192)">
       0.42
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(194,242,194)">
       0.40
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(226,249,226)">
       0.19
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(153,234,153)">
       0.67
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(241,252,241)">
       0.09
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.02
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.26
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.21
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.55
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.39
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(14012,14012,200)">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(22982,22982,165)">
       0.33
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(22816,22816,166)">
       0.33
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(839,839,252)">
       0.01
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(62470,62470,10)">
       0.74
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:left; font-weight:bold">
       n
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(206,245,206)">
       0.32
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(178,239,178)">
       0.51
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(225,249,225)">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(160,236,160)">
       0.63
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(188,241,188)">
       0.44
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.20
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.65
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right">
       0.34
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(63161,63161,7)">
       0.92
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(60897,60897,16)">
       0.89
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(21050,21050,173)">
       0.30
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(12682,12682,206)">
       0.17
      </td>
      <td style="font-size:14px; background-color:rgb(255,255,255); text-align:right; background-color:rgb(65025,65025,0)">
       0.77
      </td>
     </tr>
     <tr style="page-break-inside:avoid;">
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:left; font-weight:bold">
       o
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(170,238,170)">
       0.56
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(139,231,139)">
       0.77
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(207,245,207)">
       0.32
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(149,233,149)">
       0.70
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(127,229,127)">
       0.85
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.52
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.76
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.17
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.26
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right">
       0.52
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(16549,16549,190)">
       0.24
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(56737,56737,32)">
       0.83
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(15644,15644,194)">
       0.23
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(65025,65025,0)">
       0.91
      </td>
      <td style="font-size:14px; background-color:rgb(229,229,229); text-align:right; background-color:rgb(36722,36722,111)">
       0.43
      </td>
     </tr>
    </tbody>
   </table>
  </div>
 </body>
</html>


### Multi-index tables
Multi-index dataframes can be expanded to sinlesimple index dataframes with special formatting applied.
#### FmtExpandMultiIndex
```
FmtExpandMultiIndex(total_columns=None, operator=OP_SUM, bold=True, indent_px=20, hline_color=colors.DARK_BLUE, level_background_colors=None)
```
See example below. Can handle non-unique indices.
```
:total_columns List of columns on which to apply operator at higher index levels
:operator Computational operation to perform on columns, e.g. tf.OP_SUM, tf.OP_MEAN, tf.OP_NONE
:bold True/False, changes higher-level font-style to bold
:index_px Indentation space per level in pixels
:hline_color CSS color, sets the color of the horizontal line separating higher-level rows
:level_background_colors List of CSS colors with size equal to number of index-levels, background_color applied in each index-level row
```


    def make_multiindex_table():
        fmt = tf.FmtExpandMultiIndex()
        idx = np.array([['a', 'a', 'b', 'b'], ['aa', 'ab', 'ba', 'bb']])
        idx_tuples = list(zip(*idx))
        multi_index = pd.MultiIndex.from_tuples(idx_tuples, names=['a-level', 'aa-level'])
        columns = ['column0', 'column1', 'column2']
        data = pd.DataFrame(np.arange(12, dtype=float).reshape(4, 3), index=multi_index, columns=columns)
        return data
    
    mi_df = make_multiindex_table()
    print mi_df
    
    fmt_multiindex = tf.FmtExpandMultiIndex(operator=tf.OP_SUM)
    table_block = Block(mi_df, formatters=[fmt_multiindex], use_default_formatters=False)
    display(HTML(table_block.render_html()))

                      column0  column1  column2
    a-level aa-level                           
    a       aa              0        1        2
            ab              3        4        5
    b       ba              6        7        8
            bb              9       10       11



<!DOCTYPE html>
<html>
 <head>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_jsinflate) == 'undefined'){(function(){var zip_WSIZE=32768;var zip_STORED_BLOCK=0;var zip_STATIC_TREES=1;var zip_DYN_TREES=2;var zip_lbits=9;var zip_dbits=6;var zip_INBUFSIZ=32768;var zip_INBUF_EXTRA=64;var zip_slide;var zip_wp;var zip_fixed_tl=null;var zip_fixed_td;var zip_fixed_bl,fixed_bd;var zip_bit_buf;var zip_bit_len;var zip_method;var zip_eof;var zip_copy_leng;var zip_copy_dist;var zip_tl,zip_td;var zip_bl,zip_bd;var zip_inflate_data;var zip_inflate_pos;var zip_MASK_BITS=new Array(0x0000,0x0001,0x0003,0x0007,0x000f,0x001f,0x003f,0x007f,0x00ff,0x01ff,0x03ff,0x07ff,0x0fff,0x1fff,0x3fff,0x7fff,0xffff);var zip_cplens=new Array(3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258,0,0);var zip_cplext=new Array(0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0,99,99);var zip_cpdist=new Array(1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577);var zip_cpdext=new Array(0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13);var zip_border=new Array(16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15);var zip_HuftList=function(){this.next=null;this.list=null;}
var zip_HuftNode=function(){this.e=0;this.b=0;this.n=0;this.t=null;}
var zip_HuftBuild=function(b,n,s,d,e,mm){this.BMAX=16;this.N_MAX=288;this.status=0;this.root=null;this.m=0;{var a;var c=new Array(this.BMAX+1);var el;var f;var g;var h;var i;var j;var k;var lx=new Array(this.BMAX+1);var p;var pidx;var q;var r=new zip_HuftNode();var u=new Array(this.BMAX);var v=new Array(this.N_MAX);var w;var x=new Array(this.BMAX+1);var xp;var y;var z;var o;var tail;tail=this.root=null;for(i=0;i<c.length;i++)
c[i]=0;for(i=0;i<lx.length;i++)
lx[i]=0;for(i=0;i<u.length;i++)
u[i]=null;for(i=0;i<v.length;i++)
v[i]=0;for(i=0;i<x.length;i++)
x[i]=0;el=n>256?b[256]:this.BMAX;p=b;pidx=0;i=n;do{c[p[pidx]]++;pidx++;}while(--i>0);if(c[0]==n){this.root=null;this.m=0;this.status=0;return;}
for(j=1;j<=this.BMAX;j++)
if(c[j]!=0)
break;k=j;if(mm<j)
mm=j;for(i=this.BMAX;i!=0;i--)
if(c[i]!=0)
break;g=i;if(mm>i)
mm=i;for(y=1<<j;j<i;j++,y<<=1)
if((y-=c[j])<0){this.status=2;this.m=mm;return;}
if((y-=c[i])<0){this.status=2;this.m=mm;return;}
c[i]+=y;x[1]=j=0;p=c;pidx=1;xp=2;while(--i>0)
x[xp++]=(j+=p[pidx++]);p=b;pidx=0;i=0;do{if((j=p[pidx++])!=0)
v[x[j]++]=i;}while(++i<n);n=x[g];x[0]=i=0;p=v;pidx=0;h=-1;w=lx[0]=0;q=null;z=0;for(;k<=g;k++){a=c[k];while(a-->0){while(k>w+lx[1+h]){w+=lx[1+h];h++;z=(z=g-w)>mm?mm:z;if((f=1<<(j=k-w))>a+1){f-=a+1;xp=k;while(++j<z){if((f<<=1)<=c[++xp])
break;f-=c[xp];}}
if(w+j>el&&w<el)
j=el-w;z=1<<j;lx[1+h]=j;q=new Array(z);for(o=0;o<z;o++){q[o]=new zip_HuftNode();}
if(tail==null)
tail=this.root=new zip_HuftList();else
tail=tail.next=new zip_HuftList();tail.next=null;tail.list=q;u[h]=q;if(h>0){x[h]=i;r.b=lx[h];r.e=16+j;r.t=q;j=(i&((1<<w)-1))>>(w-lx[h]);u[h-1][j].e=r.e;u[h-1][j].b=r.b;u[h-1][j].n=r.n;u[h-1][j].t=r.t;}}
r.b=k-w;if(pidx>=n)
r.e=99;else if(p[pidx]<s){r.e=(p[pidx]<256?16:15);r.n=p[pidx++];}else{r.e=e[p[pidx]-s];r.n=d[p[pidx++]-s];}
f=1<<(k-w);for(j=i>>w;j<z;j+=f){q[j].e=r.e;q[j].b=r.b;q[j].n=r.n;q[j].t=r.t;}
for(j=1<<(k-1);(i&j)!=0;j>>=1)
i^=j;i^=j;while((i&((1<<w)-1))!=x[h]){w-=lx[h];h--;}}}
this.m=lx[1];this.status=((y!=0&&g!=1)?1:0);}}
var zip_GET_BYTE=function(){if(zip_inflate_data.length==zip_inflate_pos)
return-1;return zip_inflate_data.charCodeAt(zip_inflate_pos++)&0xff;}
var zip_NEEDBITS=function(n){while(zip_bit_len<n){zip_bit_buf|=zip_GET_BYTE()<<zip_bit_len;zip_bit_len+=8;}}
var zip_GETBITS=function(n){return zip_bit_buf&zip_MASK_BITS[n];}
var zip_DUMPBITS=function(n){zip_bit_buf>>=n;zip_bit_len-=n;}
var zip_inflate_codes=function(buff,off,size){var e;var t;var n;if(size==0)
return 0;n=0;for(;;){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);if(e==16){zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=t.n;if(n==size)
return size;continue;}
if(e==15)
break;zip_NEEDBITS(e);zip_copy_leng=t.n+zip_GETBITS(e);zip_DUMPBITS(e);zip_NEEDBITS(zip_bd);t=zip_td.list[zip_GETBITS(zip_bd)];e=t.e;while(e>16){if(e==99)
return-1;zip_DUMPBITS(t.b);e-=16;zip_NEEDBITS(e);t=t.t[zip_GETBITS(e)];e=t.e;}
zip_DUMPBITS(t.b);zip_NEEDBITS(e);zip_copy_dist=zip_wp-t.n-zip_GETBITS(e);zip_DUMPBITS(e);while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}
if(n==size)
return size;}
zip_method=-1;return n;}
var zip_inflate_stored=function(buff,off,size){var n;n=zip_bit_len&7;zip_DUMPBITS(n);zip_NEEDBITS(16);n=zip_GETBITS(16);zip_DUMPBITS(16);zip_NEEDBITS(16);if(n!=((~zip_bit_buf)&0xffff))
return-1;zip_DUMPBITS(16);zip_copy_leng=n;n=0;while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;return n;}
var zip_inflate_fixed=function(buff,off,size){if(zip_fixed_tl==null){var i;var l=new Array(288);var h;for(i=0;i<144;i++)
l[i]=8;for(;i<256;i++)
l[i]=9;for(;i<280;i++)
l[i]=7;for(;i<288;i++)
l[i]=8;zip_fixed_bl=7;h=new zip_HuftBuild(l,288,257,zip_cplens,zip_cplext,zip_fixed_bl);if(h.status!=0){alert("HufBuild error: "+h.status);return-1;}
zip_fixed_tl=h.root;zip_fixed_bl=h.m;for(i=0;i<30;i++)
l[i]=5;zip_fixed_bd=5;h=new zip_HuftBuild(l,30,0,zip_cpdist,zip_cpdext,zip_fixed_bd);if(h.status>1){zip_fixed_tl=null;alert("HufBuild error: "+h.status);return-1;}
zip_fixed_td=h.root;zip_fixed_bd=h.m;}
zip_tl=zip_fixed_tl;zip_td=zip_fixed_td;zip_bl=zip_fixed_bl;zip_bd=zip_fixed_bd;return zip_inflate_codes(buff,off,size);}
var zip_inflate_dynamic=function(buff,off,size){var i;var j;var l;var n;var t;var nb;var nl;var nd;var ll=new Array(286+30);var h;for(i=0;i<ll.length;i++)
ll[i]=0;zip_NEEDBITS(5);nl=257+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(5);nd=1+zip_GETBITS(5);zip_DUMPBITS(5);zip_NEEDBITS(4);nb=4+zip_GETBITS(4);zip_DUMPBITS(4);if(nl>286||nd>30)
return-1;for(j=0;j<nb;j++)
{zip_NEEDBITS(3);ll[zip_border[j]]=zip_GETBITS(3);zip_DUMPBITS(3);}
for(;j<19;j++)
ll[zip_border[j]]=0;zip_bl=7;h=new zip_HuftBuild(ll,19,19,null,null,zip_bl);if(h.status!=0)
return-1;zip_tl=h.root;zip_bl=h.m;n=nl+nd;i=l=0;while(i<n){zip_NEEDBITS(zip_bl);t=zip_tl.list[zip_GETBITS(zip_bl)];j=t.b;zip_DUMPBITS(j);j=t.n;if(j<16)
ll[i++]=l=j;else if(j==16){zip_NEEDBITS(2);j=3+zip_GETBITS(2);zip_DUMPBITS(2);if(i+j>n)
return-1;while(j-->0)
ll[i++]=l;}else if(j==17){zip_NEEDBITS(3);j=3+zip_GETBITS(3);zip_DUMPBITS(3);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}else{zip_NEEDBITS(7);j=11+zip_GETBITS(7);zip_DUMPBITS(7);if(i+j>n)
return-1;while(j-->0)
ll[i++]=0;l=0;}}
zip_bl=zip_lbits;h=new zip_HuftBuild(ll,nl,257,zip_cplens,zip_cplext,zip_bl);if(zip_bl==0)
h.status=1;if(h.status!=0){if(h.status==1);return-1;}
zip_tl=h.root;zip_bl=h.m;for(i=0;i<nd;i++)
ll[i]=ll[i+nl];zip_bd=zip_dbits;h=new zip_HuftBuild(ll,nd,0,zip_cpdist,zip_cpdext,zip_bd);zip_td=h.root;zip_bd=h.m;if(zip_bd==0&&nl>257){return-1;}
if(h.status==1){;}
if(h.status!=0)
return-1;return zip_inflate_codes(buff,off,size);}
var zip_inflate_start=function(){var i;if(zip_slide==null)
zip_slide=new Array(2*zip_WSIZE);zip_wp=0;zip_bit_buf=0;zip_bit_len=0;zip_method=-1;zip_eof=false;zip_copy_leng=zip_copy_dist=0;zip_tl=null;}
var zip_inflate_internal=function(buff,off,size){var n,i;n=0;while(n<size){if(zip_eof&&zip_method==-1)
return n;if(zip_copy_leng>0){if(zip_method!=zip_STORED_BLOCK){while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_copy_dist&=zip_WSIZE-1;zip_wp&=zip_WSIZE-1;buff[off+n++]=zip_slide[zip_wp++]=zip_slide[zip_copy_dist++];}}else{while(zip_copy_leng>0&&n<size){zip_copy_leng--;zip_wp&=zip_WSIZE-1;zip_NEEDBITS(8);buff[off+n++]=zip_slide[zip_wp++]=zip_GETBITS(8);zip_DUMPBITS(8);}
if(zip_copy_leng==0)
zip_method=-1;}
if(n==size)
return n;}
if(zip_method==-1){if(zip_eof)
break;zip_NEEDBITS(1);if(zip_GETBITS(1)!=0)
zip_eof=true;zip_DUMPBITS(1);zip_NEEDBITS(2);zip_method=zip_GETBITS(2);zip_DUMPBITS(2);zip_tl=null;zip_copy_leng=0;}
switch(zip_method){case 0:i=zip_inflate_stored(buff,off+n,size-n);break;case 1:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_fixed(buff,off+n,size-n);break;case 2:if(zip_tl!=null)
i=zip_inflate_codes(buff,off+n,size-n);else
i=zip_inflate_dynamic(buff,off+n,size-n);break;default:i=-1;break;}
if(i==-1){if(zip_eof)
return 0;return-1;}
n+=i;}
return n;}
var zip_inflate=function(str){var i,j;zip_inflate_start();zip_inflate_data=str;zip_inflate_pos=0;var buff=new Array(1024);var aout=[];while((i=zip_inflate_internal(buff,0,buff.length))>0){var cbuf=new Array(i);for(j=0;j<i;j++){cbuf[j]=String.fromCharCode(buff[j]);}
aout[aout.length]=cbuf.join("");}
zip_inflate_data=null;return aout.join("");}
if(!window.RawDeflate)RawDeflate={};RawDeflate.inflate=zip_inflate;})();_pybloqs_load_sentinel_jsinflate = true;}
  </script>
  <script type="text/javascript">
   if(typeof(_pybloqs_load_sentinel_block_core) == 'undefined'){function isIE(){var myNav=navigator.userAgent.toLowerCase();return(myNav.indexOf('msie')!=-1)?parseInt(myNav.split('msie')[1]):false;}
var ieVersion=isIE();if(ieVersion&&ieVersion<10){alert("Internet Explorer 10 and older are not supported. Use Chrome, Firefox, Safari or IE 11 instead.");}
function blocksEval(data){(window.execScript||function(data){window["eval"].call(window,data);})(data);}
function registerWaitHandle(handle){if(!window.loadWaitHandleRegistry){window.loadWaitHandleRegistry={}}
loadWaitHandleRegistry[handle]=false;}
function setLoaded(handle){loadWaitHandleRegistry[handle]=true;}
function runWaitPoller(){var loadWaitPoller=setInterval(function(){if("loadWaitHandleRegistry"in window){var handleCount=0;for(var handle in loadWaitHandleRegistry){if(!loadWaitHandleRegistry.hasOwnProperty(handle)){handleCount++;if(!loadWaitHandleRegistry[handle]){return}}}}
clearInterval(loadWaitPoller);window.print();},10);return loadWaitPoller;}_pybloqs_load_sentinel_block_core = true;}
  </script>
  <style type="text/css">
   .pybloqs {
    font-family: Helvetica, "Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, sans-serif;
}

.pybloqs pre code {
    display: block;
    margin-left: 1em;
    font-family: monospace;
}
  </style>
 </head>
 <body>
  <div class="pybloqs">
   <table border="0" cellpadding="1" cellspacing="0" style="">
    <thead style="">
     <tr style="">
      <th style="">
      </th>
      <th style="">
       column0
      </th>
      <th style="">
       column1
      </th>
      <th style="">
       column2
      </th>
     </tr>
    </thead>
    <tbody>
     <tr style="">
      <td style="padding-left:0px; font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       a
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       3.0
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       5.0
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       7.0
      </td>
     </tr>
     <tr style="">
      <td style="padding-left:20px">
       aa
      </td>
      <td style="">
       0.0
      </td>
      <td style="">
       1.0
      </td>
      <td style="">
       2.0
      </td>
     </tr>
     <tr style="">
      <td style="padding-left:20px">
       ab
      </td>
      <td style="">
       3.0
      </td>
      <td style="">
       4.0
      </td>
      <td style="">
       5.0
      </td>
     </tr>
     <tr style="">
      <td style="padding-left:0px; font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       b
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       15.0
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       17.0
      </td>
      <td style="font-weight:bold; border-bottom:1px solid rgb(30,51,124); border-top:1px solid rgb(30,51,124)">
       19.0
      </td>
     </tr>
     <tr style="">
      <td style="padding-left:20px">
       ba
      </td>
      <td style="">
       6.0
      </td>
      <td style="">
       7.0
      </td>
      <td style="">
       8.0
      </td>
     </tr>
     <tr style="">
      <td style="padding-left:20px">
       bb
      </td>
      <td style="">
       9.0
      </td>
      <td style="">
       10.0
      </td>
      <td style="">
       11.0
      </td>
     </tr>
    </tbody>
   </table>
  </div>
 </body>
</html>


###Writing custom formatters
Custom formatters can either be either added to pybloqs or included with user-space code. The latter is useful for very specific formatters, which have little chance of being reused and thus do not need to sit in the code base.
In general, formatters are classes that inherit from ```TableFormatter``` base class. The base class provides the following function hooks, which do not need to be all implemented by the new formatter. In fact, most formatters only make use of one or two function hooks. The available hooks are:
* ```_insert_additional_html```: Can be used to put HTML or JavaScript code in front of table.
* ```_modify_dataframe```: Access and potentially modify DataFrame before any other hook functions become active.
* ```_modify_cell_content```: Access and potentially modify cell value. Called for each cell separately. 
* ```create_table_level_css```: Insert CSS inline style on ```<table>``` level
* ```_create_thead_level_css```: Insert CSS inline style on ```<thead>``` level
* ```_create_row_level_css```: Insert CSS inline style on ```<th>``` and ```<tr>```level
* ```_create_cell_level_css```: Insert CSS inline style on ```<td>``` level



    
