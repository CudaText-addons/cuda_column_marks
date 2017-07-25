from cudatext import *

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


class Command:
    def jump_left(self):
        do_jump(False)

    def jump_right(self):
        do_jump(True)

    def set_marks(self):
        s = ed.get_prop(PROP_MARGIN_STRING)
        s = dlg_input('Column marks (space separated):', s)
        if s is None: return
        ed.set_prop(PROP_MARGIN_STRING, s)
        ed_bro.set_prop(PROP_MARGIN_STRING, s)
