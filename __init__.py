from cudatext import *
import cudax_lib as apx
import cudatext_cmd as cmds

def do_jump(is_next):
    carets = ed.get_carets()
    if len(carets)>1:
        msg_status('Need single caret')
        return
    x, y, x2, y2 = carets[0]

    s = ed.get_prop(PROP_MARGIN_STRING).strip()
    if s:
        s = s.split(' ')
        s = list(map(int, s))
    else:
        s = []

    #add 0 and fixed margin
    s += [0, ed.get_prop(PROP_MARGIN)]
    s = sorted(s)

    #recalc if tab-chars present
    s2 = []
    for i in s:
        ii, _ = ed.convert(CONVERT_COL_TO_CHAR, i, y, ed.get_text_line(y))
        s2 += [ii]
    s = s2


    if is_next:
        while s and s[0]<=x: del s[0]
        x = s[0] if s else -1
    else:
        while s and s[-1]>=x: del s[-1]
        x = s[-1] if s else -1

    if x<0:
        msg_status('Cannot jump to mark')
        return

    ed.set_caret(x, y, x2, y2)
    msg_status('Jumped to column %d' % x)

def ed_bro(ed):
    h_self = ed.get_prop(PROP_HANDLE_SELF)
    h_pri = ed.get_prop(PROP_HANDLE_PRIMARY)
    h_sec = ed.get_prop(PROP_HANDLE_SECONDARY)
    if h_self==h_pri:
        return Editor(h_sec)
    else:
        return Editor(h_pri)

class Command:
    def jump_left(self):
        do_jump(False)

    def jump_right(self):
        do_jump(True)

    def set_margin(self):
        s = ed.get_prop(PROP_MARGIN)
        s = dlg_input('Fixed margin value.\nPrefix with "!" to save permamently.', str(s))
        if s is None: return
        save = s.startswith('!')
        if save:
            s = s[1:]

        try:
            n = int(s)
            ed.set_prop(PROP_MARGIN, n)
            ed_bro(ed).set_prop(PROP_MARGIN, n)
        except:
            return msg_status('Wrong integer value: '+s)

        if save:
            apx.set_opt('margin', n)
            ed.cmd(cmds.cmd_OpsReloadAndApply)

    def set_margins(self):
        s = ed.get_prop(PROP_MARGIN_STRING)
        s = dlg_input('Additional margins (space separated).\nPrefix with "!" to save permamently.', str(s))
        if s is None: return
        save = s.startswith('!')
        if save:
            s = s[1:]

        ed.set_prop(PROP_MARGIN_STRING, s)
        ed_bro(ed).set_prop(PROP_MARGIN_STRING, s)

        if save:
            apx.set_opt('margin_string', s)
            ed.cmd(cmds.cmd_OpsReloadAndApply)
