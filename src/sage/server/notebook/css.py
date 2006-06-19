"""
SAGE Notebook CSS
"""

import os

from sage.misc.misc import DOT_SAGE

def css(color='default'):
    """
    Return the CSS header used by the SAGE Notebook.

    INPUT:
        color -- string or pair of html colors, e.g.,
                    'gmail'
                    'grey'
                    ('#ff0000', '#0000ff')

    EXAMPLES:
        sage: import sage.server.notebook.css as c
        sage: type(c.css())
        <type 'str'>
    """
    s = r"""
/**** TOP CONTROL BAR ************************/

div.top_control_bar {
   z-index: 0;
   background-color: white;
   position: fixed;
   left: 0px;
   width: 100%;
   top: 0px;
   padding-left: 2ex;
}

span.control_commands {
   position: fixed;
   top:1ex;
   right:1ex;
   text-align:right;
   color:blue;
   font-weight:normal;
   font-family:arial;
   font-size:12px;
/*    text-decoration:underline; */
}

span.vbar {
   height:1.5ex;
   border-left:1px solid black;
   width:1px;
}

div.top_control_bar a.evaluate {
   background-color:white;
   padding:5;
   text-decoration:underline;
}

div.top_control_bar a.evaluate:hover {
   background-color:#00bb00;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.interrupt {
/*   text-decoration: underline;
   font-family:arial;
   font-size:12px;
   font-weight:bold;
   color:#000000;
   */
   text-decoration:underline;
   padding:5;
   background-color:white;
}

div.top_control_bar a.interrupt:hover {
   background-color:#bb0000;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.interrupt_grey {
   color:#888888;
   padding:5;
   background-color:white;
}

div.top_control_bar  a.interrupt_in_progress {
   color:#FFFFFF;
   padding:5;
   background-color:#bb0000;
   text-decoration:blink;
   text-decoration:underline;
}

div.top_control_bar  a.hide{
   background-color:white;
   padding:5;
   text-decoration:underline;
}

div.top_control_bar a.hide:hover {
   background-color:#0000bb;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.help {
   padding:5;
   background-color:white;
   text-decoration:underline;
}

div.top_control_bar a.help:hover {
   background-color:#00bb00;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.plain_text {
   padding:5;
   background-color:white;
   text-decoration:underline;
}

div.top_control_bar a.plain_text:hover {
   background-color:#00bb00;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.doctest_text {
   padding:5;
   background-color:white;
   text-decoration:underline;
}

div.top_control_bar a.doctest_text:hover {
   background-color:#0044bb;
   color:#FFFFFF;
   cursor:pointer;
}


div.top_control_bar  a.history_link {
   padding:5;
   background-color:white;
   text-decoration:underline;
}

div.top_control_bar a.history_link:hover {
   background-color:995533;
   color:#FFFFFF;
   cursor:pointer;
}

div.top_control_bar  a.download_sws {
   padding:5;
   background-color:white;
   text-decoration:underline;
}

div.top_control_bar a.download_sws:hover {
   background-color:#55bb22;
   color:#FFFFFF;
   cursor:pointer;
}

/***** SEARCH / HELP AREA *********************************/

span.search_doc_topbar {
   z-index: 12;
   height: 24px;
   font-family:courier;
   font-size: 12px;
   width:158px;
   top: 40px;
   left: 5px;
   position: fixed;
   border:1px solid #387CAF;
   background-color: #73a6ff;
}

td.menubar{
   text-decoration: none;
   font-family:arial;
   font-size:15px;
   font-weight:bold;
   color:#FFFFFF;
}

a.menubar{
   text-decoration: none;
   font-family:arial;
   font-size:15px;
   font-weight:bold;
   color:#FFFFFF;
   background-color:#73a6ff;
}

input.search_input {
   position: fixed;
   left: 5px;
   top: 65px;
   height: 32px;
   width: 160px;
   padding: 4px;
   z-index: 12;
   font-family:courier;
   font-size:14px;
   color: #222222;
   color: #808080;
   border: 3px solid #387CAF;
   background: #FFF;
}

span.search_doc {
   z-index: 12;
   font-family:arial;
   font-size:12px;
   overflow:auto;
   position: fixed;
   top: 96px;
   left: 5px;
   width: 154px;
   height: 150px;
   margin: 0px;
   border:1px solid #387CAF;
   background-color: white;
   padding: 2px;
}


/************ INFO PANES **************************/

span.pane {
   z-index:30;
   font-family:courier, monospace;
   font-size:12px;
   position: fixed;
   left: 1em;
   top: 33px;
   width: 180px;
   height:100%;
   margin: 0px;
   padding-right: 2px;
   padding-left: 2px;
   padding-top: 0px;
   bottom: 0ex;
}



/************ VARIABLES **************************/

span.pane div.variables_topbar {
   color:black;
   background-color: <color1>;
   font-family:arial;
   text-decoration: none;
   font-size:13px;
   height: 2ex;
   padding-left: 10px;
   margin:0;
   width: 174px;
}

span.pane div.variables_list {
   font-size:11px;
   top:0ex;
   height:20ex;
   border:2px solid <color1>;
   width: 180px;
   overflow:auto;
}

div.variable_name {
   padding-left:1ex;
   border-top:1px solid #d3e9ff;
}

/*div.variable_name:hover {
   background-color:<color1>;
   cursor:pointer;
}*/

span.varname {
}

span.vartype {
  /* color:#888888; */
  color:#657d6c;
}

/************ ATTACHED **************************/

span.pane div.attached_topbar {
   color: black;
   height: 2ex;
   top: 0ex;
   background-color: <color1>;
   text-decoration: none;
   font-size:13px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
}

span.pane div.attached_list {
   font-size:11px;
   top:0ex;
   height:20ex;
   border:2px solid  <color1>;
   width: 180px;
   overflow:auto;
}

div.attached_filename {
   padding-left:1ex;
   border-top:1px solid #d3e9ff;
}
/*
div.attached_filename:hover {
   background-color:<color1>;
   cursor:pointer;
}
*/

/************ WORKSHEETS **************************/

span.pane div.worksheets_topbar {
   color:black;
   height: 2ex;
   top: 0ex;
   background-color: <color2>;
   text-decoration: none;
   font-size:12px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
}

span.X {
   color:white;
   font-family:arial monospace;
   font-weight:bold;
   cursor:pointer;
}

span.pane div.add_new_worksheet_menu {
   color:black;
   top: 0ex;
   background-color: <color2>;
   text-decoration: none;
   font-size:11px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
   display:none;
}

input.add_new_worksheet_menu {
   width:60%
}

button.add_new_worksheet_menu {
   font-size:11px;
   font-family:arial;
}

span.pane div.upload_worksheet_menu {
   color:black;
   top: 0ex;
   background-color: <color2>;
   text-decoration: none;
   font-size:11px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
   display:none;
}

button.upload_worksheet_menu {
   font-size:11px;
   font-family:arial;
}

input.upload_worksheet_menu {

}

span.pane div.delete_worksheet_menu {
   color:black;
   top: 0ex;
   background-color: <color2>;
   text-decoration: none;
   font-size:11px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
   display:none;
}

input.delete_worksheet_menu {
   width:50%
}

button.delete_worksheet_menu {
   font-size:11px;
   font-family:arial;
   background-color: #ffcccc;
}

span.pane div.worksheet_list {
   font-size:11px;
   top:0ex;
   height:25ex;
   border:2px solid <color2>;
   overflow:auto;
   width: 180px;
}

a.new_worksheet {
   font-family: arial, monospace;
   font-size:8pt;
   text-decoration:underline;
   text-align:right;
   color: #0000aa
}

a.new_worksheet:hover {
  cursor:pointer;
}

div.worksheet_bottom_padding {
   height:50%;
}

div.worksheet_top_padding {
   height:5%;
}

div.worksheet_title {
   z-index:2;
   top:36px;
   padding-top: 3px;
   padding-left: 1em;
   background-color: <color1>;
   width: 100%;
   font-family:arial;
   font-size: 16px;
   font-weight:bold;
   color:black;
   position: fixed;
}

div.worksheet_title_under {
   z-index:0;
   padding-top: 3px;
   padding-left: 1em;
   background-color: <color1>;
   width: 100%;
   font-family:arial;
   font-size: 22px;
   font-weight:bold;
   color:black;
}

div.worksheet_cell_list {
}

a.delete_worksheet {
   font-family: arial, monospace;
   font-size:8pt;
   text-decoration:underline;
   text-align:right;
   color: #0000aa
}

a.delete_worksheet:hover {
  cursor:pointer;
}

a.upload_worksheet {
   font-family: arial, monospace;
   font-size:8pt;
   text-decoration:underline;
   text-align:right;
   color: #0000aa
}

a.upload_worksheet:hover {
  cursor:pointer;
}

span.pane a.worksheet_current {
   font-size:11px;
   padding-left:1ex;
   border-top:1px solid <color2>;
   background-color:<color2>;
   text-decoration:none;
   color:black;
 }

span.pane a.worksheet_current_computing {
   font-size:11px;
   padding-left:1ex;
   border-top:1px solid <color1>;
   background-color:#ffd1d1;
   text-decoration:none;
   color:black;
 }

span.pane a.worksheet_other {
   font-size:11px;
   padding-left:1ex;
   border-top:1px solid <color2>;
   background-color:white;
   text-decoration:none;
   color:black;
}

span.pane a.worksheet_other:hover {
   background-color:<color2>;
   text-decoration:none;
   cursor:pointer;
}

span.pane a.worksheet_other_computing {
   font-size:11px;
   padding-left:1ex;
   border-top:1px solid <color1>;
   background-color:ffd1d1;
   text-decoration:none;
   color:black;
}

/************ OBJECTS **************************/

span.pane div.objects_topbar {
   color:black;
   height: 2ex;
   top: 0ex;
   background-color: <color2>;
   text-decoration: none;
   font-size:13px;
   font-family:arial;
   padding-left: 10px;
   width: 174px;
}

span.pane div.object_list {
   font-size:11px;
   height:20ex;
   border:2px solid <color2>;
   width: 180px;
   overflow:auto;
}

a.object_name {
   padding-left:1ex;
   border-top:1px solid <color2>;
   background-color:white;
   text-decoration:none;
   color:black;
}

a.object_name:hover {
   background-color:<color2>;
   text-decoration:none;
   color:black;
   cursor:pointer;
}



/************ CONTROLS **************************/

div.control_area{
    vertical-align: top;
}

span.control {
    border:1px solid white;
    font-family: courier, monospace;
    font-size:14pt;
    font-weight:bold;
}

span.control a.cs {
    color:#777777;
    text-decoration:none;
    border:0px solid white;
}

span.control:hover a.cs, span.control a:hover.cs {
    color:black;
    border:1px solid #333333;
}

/************ WORKSHEET **************************/

div.worksheet {
  position:fixed;
  overflow:auto;
  z-index:1;
  background-color: white;
  border-top: 0px;
  border-left: 10px solid <color1>;
  top: 58px;
  bottom: 0ex;
  right: 0ex;
  left: 205px;
  padding-left: 0ex;
  float: right;
  padding-top: 0ex;
}


span.banner{
  background-color:white;
  font-family:arial;
  font-size:30px;
  text-decoration: none;
  font-weight: bold;
  color: #387CAF;
  margin: 0px;
}


input.btn {
  font-family: courier;
  font-size:13pt;
  font-weight:bold;
  color:#808080;
  text-decoration:none;
  background: white;
  padding:0px;
  margin:0px;
  border:1px solid white;
}
input.btn:hover {
  color: black;
  text-decoration: none;
  background: white;
  padding: 0px;
  margin: 0px;
  border: 1px solid #333333;
}

/************ CELL INPUT **************************/

td.cell_number {
   font-size:8pt;
   font-family:arial, monospace;
   color:#999999;
   text-align:left;
   cursor:pointer;
}

td.output_cell {
   width:100%;
}

div.cellbox {
  z-index:2;
  background-color: white;
  padding-left: .5em;
  padding-top: 1.5em;
}

pre.cell_input_pre {
  background-color: white;
  border: 0px solid #ffffff;
  font-family: courier, monospace;
  font-size:12pt;
  overflow:hidden;
  padding-left:0px;
  padding-top:0px;
  padding-bottom:0px;
  width: 100%;
}

textarea.cell_input {
  background-color: white;
  border: 0px solid #ffffff;
  font-family: courier, monospace;
  font-size:12pt;
  overflow:hidden;
  padding-left:3px;
  padding-top:0px;
  padding-bottom:0px;
  width: 100%;
}

textarea.cell_input_hide {
  background-color: white;
/*  color:#999999; */
  color:#cccccc;
  border: 0px solid #ffffff;
  border-top: 1px solid #aaaaff;
  border-bottom: 1px solid #aaaaff;
  font-family: courier, monospace;
  font-size:12pt;
  overflow:hidden;
  padding-left:3px;
  padding-top:0px;
  padding-bottom:0px;
  width: 100%;
  height:1.2em;
}

textarea.cell_input_active {
  background-color: white;
 /* border: 2px solid #73a6ff; */
   border: 0px solid #ffffff;
  font-family: courier, monospace;
  font-size:12pt;
  overflow:hidden;
  padding-left:3px;
  padding-top:0px;
  padding-bottom:0px;
  width: 100%;
}



/************ CELL OUTPUT **************************/
/* This is complicated and redundant but it makes
   the other Python and Javascript code way simpler,
   and you have a lot of options for customizability. */

div.cell_output {
  font-family: courier, monospace;
  font-size:12pt;
  width: 95%;
  margin: 0px;
  padding: 0px;
 /* border-left: 1px solid #aaaaff;  */
}

table.cell_output_box {
  margin:0px;
  padding:0px;
  border-top:1px solid #cccccc;
  border-bottom:1px solid #cccccc;
}

pre.cell_output_wrap {
  font-family: courier, monospace;
  font-size:12pt;
  margin:0px;
  padding:0px;
  color:#000088;
}
pre.cell_output_nowrap {
  display:none;
}
pre.cell_output_hidden {
  display:none;
}


pre.cell_output_nowrap_wrap {
  display:none;
}
pre.cell_output_nowrap_nowrap {
  font-family: courier, monospace;
  font-size:12pt;
  margin:0px;
  padding:0px;
  color:#000088;
}
pre.cell_output_nowrap_hidden {
  display:none;
}

span.cell_output_html_wrap {
  font-family: courier, monospace;
  font-size:12pt;
}

span.cell_output_html_nowrap {
  font-family: courier, monospace;
  font-size:12pt;
}

span.cell_output_html_hidden {
   display:none;
}

div.cell_output_running {
  font-family: courier, monospace;
  font-size:12pt;
  width: 100%;
  margin: 0px;
  /* border-left: 2px solid #880000;  */
  background-color: <color2>;
  border: 1px solid <color2>;
}

div.cell_output_running:hover {
  /*  cursor:wait;*/
}


div.cell_output_hidden {
  width: 100%;
  height: 3px;
  margin: 0px;
  border-left: 4em solid #aaaaaa;
/*   border-top: 1px solid <color1>;
  border-bottom: 1px solid <color1>;
  */
}

pre.cell_output_hidden {
  display: none;
}

pre.cell_output_hide {
  display:none;
}


/************ INSERTING NEW CELLS **************************/

div.insert_new_cell {
  height:4px;
  width:100%;
  border-top: 2px solid white;
  display:block;
}

div.insert_new_cell:hover {
  border-top: 2px solid #000000;
  /* background-color:#eeeeee; */
}
"""
    if color == 'gmail':
        color1 = '#c3d9ff'
        color2 = '#b5edbc'
    elif color == 'grey':
        color1 = '#aaaaaa'
        color2 = '#888888'
    elif color == 'default' or color == None:
        color1 = '#dedede'
        color2 = '#b5edbc'
    elif isinstance(color, (tuple,list)):
        color1, color2 = color
    else:
        raise ValueError, "unknown color scheme %s"%color

    s = s.replace('<color1>',color1).replace('<color2>',color2)
    user_css = DOT_SAGE + '/notebook.css'
    if os.path.exists(user_css):
        s += '\n' + open(user_css).read()

    return s
