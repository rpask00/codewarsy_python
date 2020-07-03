import functools
import itertools


def flat_list(arr):
    send_back = []
    for i in arr:
        if type(i) == list:
            send_back += flat_list(i)
        else:
            send_back.append(i)
    return send_back


def insert_plus(seq, a):
    operators = ['+', '-', '*', '/']
    if type(seq) == str:
        seq = [seq]

    if a not in operators and seq[-1] not in operators:
        seq.append('+')

    seq.append(a)

    return seq


def calc(expression):
    stack = []
    current_index = 0
    while True:
        if not expression.count('('):
            break

        if not current_index:
            current_index = expression.index('(')

        for i, c in enumerate(expression[current_index+1:]):
            if c == '(':
                current_index += i+1
                break

            if c == ')':
                stack.append(expression[current_index+1: current_index + i + 1])
                expression = expression[:current_index] + f'${len(stack)-1}$' + expression[current_index + i+2:]
                current_index = 0
                break

    for i, s in enumerate(stack):
        if not s.count('$'):
            stack[i] = solve_expression(split_expression(clear_expression(s)))
        else:
            insert_index = s.index('$') + 1
            insert_value = str(stack[int(s[insert_index])])
            stack[i] = s[:insert_index-1] + insert_value + s[insert_index+2:]

    for i, s in enumerate(stack):
        if type(s) == str:
            stack[i] = solve_expression(split_expression(clear_expression(s)))

    while expression.count('$'):
        insert_index = expression.index('$') + 1
        insert_value = str(stack[int(expression[insert_index])])
        expression = expression[:insert_index-1] + insert_value + expression[insert_index+2:]

    return solve_expression(split_expression(clear_expression(expression)))


def clear_expression(exp):
    exp = exp.replace(' ', '')
    exp = exp.replace('(', '')
    exp = exp.replace(')', '')
    exp = exp.replace('e', '')
    exp = exp.replace('---', '-')
    exp = exp.replace('*--', '*')
    exp = exp.replace('/--', '/')
    exp = exp.replace('+--', '+')
    exp = exp.replace('-+', '-')
    exp = exp.replace('+-', '-')
    exp = exp.replace(' ', '')
    exp = exp.replace('/', ' / ')
    exp = exp.replace('+', ' + ')
    exp = exp.replace('*', ' * ')
    exp = exp.split(' ')
    return exp


def split_expression(exp):
    for i, e in enumerate(exp):
        if e.count('-'):
            e = e.replace('-', ' -')
        exp[i] = [ee for ee in e.split(' ') if ee]

    exp = functools.reduce(insert_plus, flat_list(exp))

    return [exp] if type(exp) == str else exp


def solve_expression(exp):
    if exp[0] == '-':
        exp.insert(0, 0)

    while len(exp) > 1:
        for i, e in enumerate(exp):
            if e == '*':
                exp[i-1] = float(exp.pop(i-1)) * float(exp.pop(i))
            elif e == '/':
                exp[i - 1] = float(exp.pop(i - 1)) / float(exp.pop(i))

            elif not exp.count('*') and not exp.count('/'):
                if e == '+':
                    exp[i-1] = float(exp.pop(i-1)) + float(exp.pop(i))
                elif e == '-':
                    exp[i - 1] = float(exp.pop(i - 1)) - float(exp.pop(i))
                else:
                    continue
            else:
                continue
            break

    return float(exp[0])


tests = [
    {
        "exp": "-50/-43+64/15+67-16*-85--33",
        "result": "1465.429457364341"
    },
    {
        "exp": "-36+17+70+57*52-20-61-13",
        "result": "2921"
    },
    {
        "exp": "62*3+-61*40/-97+38+68-74",
        "result": "243.15463917525773"
    },
    {
        "exp": "-39-26*91*-3*94-92*99/83",
        "result": "667063.265060241"
    },
    {
        "exp": "97/-94/79*97*44/31--41*-70",
        "result": "-2871.798371893"
    },
    {
        "exp": "-4+-51*-61--27+57+30*4/15",
        "result": "3199.0"
    },
    {
        "exp": "-67*32+-27/55-29+-91+-92*11",
        "result": "-3276.490909090909"
    },
    {
        "exp": "22/8-62*-10*-80--86-16/90",
        "result": "-49511.427777777775"
    },
    {
        "exp": "25+-1-46/25--67/-64+55*-16",
        "result": "-858.886875"
    },
    {
        "exp": "85+-93+-55-98/-85-44+-40+77",
        "result": "-68.84705882352941"
    },
    {
        "exp": "-40+-77+12/12*45--65+34+-59",
        "result": "-32.0"
    },
    {
        "exp": "4*-51-23*-89/-91*-51/-55/29",
        "result": "-204.71926005029454"
    },
    {
        "exp": "-27-47/36--52-61+-100*88/50",
        "result": "-213.30555555555554"
    },
    {
        "exp": "-63-92--52/13*57/92-16*-39",
        "result": "471.47826086956525"
    },
    {
        "exp": "-59/-49-57*-45-52/-58--43+90",
        "result": "2700.100633356791"
    },
    {
        "exp": "-27-83*-57/-4*98+-93--70--77",
        "result": "-115882.5"
    },
    {
        "exp": "-12--93--90+-46--30+84+-92+-85",
        "result": "62"
    },
    {
        "exp": "-80/-20-64+-8/81*99+-50*1",
        "result": "-119.77777777777777"
    },
    {
        "exp": "-84*91/-67*11+-46+-16/-58*-87",
        "result": "1184.9850746268655"
    },
    {
        "exp": "-50*-51*-86+-32-100--91/34+59",
        "result": "-219370.32352941178"
    },
    {
        "exp": "78/22*-34/-73--81*-24-85--47",
        "result": "-1980.348692403487"
    },
    {
        "exp": "-26-5-6--55-90+14+66-2",
        "result": "6"
    },
    {
        "exp": "-28/58/-39--42--11*99*59/-66",
        "result": "-931.4876215738285"
    },
    {
        "exp": "28*88--38+54*97*-6*80/24",
        "result": "-102258.0"
    },
    {
        "exp": "81/75*22--82+61+81*-52--55",
        "result": "-3990.24"
    },
    {
        "exp": "28+6-9+40/43--74/100*95",
        "result": "96.23023255813953"
    },
    {
        "exp": "-84-78/4*50*-67+7-39*-28",
        "result": "66340.0"
    },
    {
        "exp": "87*-2+-27--66+94/-31--64+-96",
        "result": "-170.03225806451613"
    },
    {
        "exp": "14+-34-51/-15*-36/35*-97-56",
        "result": "263.2228571428571"
    },
    {
        "exp": "-33-14*-10*7*85/53+-13/-27",
        "result": "1539.1795946890286"
    },
    {
        "exp": "-70*67*58/-13/83+-52/79-42",
        "result": "209.4455719665419"
    },
    {
        "exp": "70*-79/75-14/-91-7/6--5",
        "result": "-69.74615384615385"
    },
    {
        "exp": "32+-35*72+-5*49*95/64+-49",
        "result": "-2900.671875"
    },
    {
        "exp": "-67-13+-93*-27*37+-50+96*95",
        "result": "101897"
    },
    {
        "exp": "-84+24/-91*76+80*-48+-74+53",
        "result": "-3965.043956043956"
    },
    {
        "exp": "78/84*6/-87*-55/94+59*9",
        "result": "531.0374698668903"
    },
    {
        "exp": "7--50+-16-29+-84/51/-55*97",
        "result": "14.904812834224598"
    },
    {
        "exp": "-80+16-90--53+-39+83/83/3",
        "result": "-139.66666666666666"
    },
    {
        "exp": "11*-11/-72+69+-15*-91-84+5",
        "result": "1356.6805555555557"
    },
    {
        "exp": "2--17/-64/-34*6--78/13/95",
        "result": "2.1100328947368423"
    },
    {
        "exp": "67/70/9-19--76--23-6-73",
        "result": "1.1063492063492077"
    },
    {
        "exp": "87-53/-12+-21*-7-45/75--77",
        "result": "314.8166666666667"
    },
    {
        "exp": "82/66+38--80--97+94-25+51",
        "result": "336.24242424242425"
    },
    {
        "exp": "69-16--72-34+-20-2--78*90",
        "result": "7089"
    },
    {
        "exp": "5--100+-5*79+73/56+-36-34",
        "result": "-358.69642857142856"
    },
    {
        "exp": "49/-83+33+-11+-70/23+-32*30",
        "result": "-941.6338397066527"
    },
    {
        "exp": "15*51*-78+-52/71-13-66/-26",
        "result": "-59681.19393282774"
    },
    {
        "exp": "11/-38/13-30/-89*29/71*99",
        "result": "13.608054046885142"
    },
    {
        "exp": "25+40/-28--26*-23*-60*-92*-10",
        "result": "33009623.57142857"
    },
    {
        "exp": "50+66--89--33+-7*-9*23+68",
        "result": "1755"
    },
    {
        "exp": "-76-82*-43+-83--24+34/32--86",
        "result": "3478.0625"
    },
    {
        "exp": "-78--59*-28*70-6/-48*-95/-35",
        "result": "-115717.66071428571"
    },
    {
        "exp": "40*-37/-58+-28--78+58/-75/-27",
        "result": "75.545883354619"
    },
    {
        "exp": "-57+77+2*54/2*13*-75*-83",
        "result": "4369970.0"
    },
    {
        "exp": "-24+69--97-38+-82/-80+-45/11",
        "result": "100.93409090909091"
    },
    {
        "exp": "-94-80/70+83-67*15/68+-98",
        "result": "-124.92226890756302"
    },
    {
        "exp": "94/96+-36+22+-83--30+-96/78",
        "result": "-67.25160256410257"
    },
    {
        "exp": "92/-26/-7/-87/-74/56+14--87",
        "result": "101.000001402095"
    },
    {
        "exp": "33--22--48/-55--44*49*6/-89",
        "result": "-91.22104187946886"
    },
    {
        "exp": "5*-5/-2+22*-79*52*-10+-68",
        "result": "903704.5"
    },
    {
        "exp": "-67-95*-8*80+-5+76/-93--76",
        "result": "60803.18279569892"
    },
    {
        "exp": "84-42+-52+98+-69+-44*4--70",
        "result": "-87"
    },
    {
        "exp": "92*-4+-53--90+11/75/22+-72",
        "result": "-402.99333333333334"
    },
    {
        "exp": "46--32+-69-31--90/-63/-33-80",
        "result": "-101.95670995670996"
    },
    {
        "exp": "47*10/-37-71*-100/36+71*-20",
        "result": "-1235.4804804804805"
    },
    {
        "exp": "-90*-91*-61*-79+71--60*-7/81",
        "result": "39467675.81481481"
    },
    {
        "exp": "-15+-52*57--99+74+-3--65+-93",
        "result": "-2837"
    },
    {
        "exp": "23-63--89/38--33+-36*-47--93",
        "result": "1780.342105263158"
    },
    {
        "exp": "49+-16/-78/-25--56-47/88-69",
        "result": "35.45770396270396"
    },
    {
        "exp": "-51*-70+-2-29*-95--55--46/28",
        "result": "6379.642857142857"
    },
    {
        "exp": "69/-49/-11/41/-11*-9--69-63",
        "result": "6.002554619912871"
    },
    {
        "exp": "73+-85*14--18/-22--100*29*-57",
        "result": "-166417.81818181818"
    },
    {
        "exp": "-16/63+-63/85+18+98+14*52",
        "result": "843.0048552754436"
    },
    {
        "exp": "56/6+45*-85--51--34*71*-21",
        "result": "-54458.666666666664"
    },
    {
        "exp": "91+-44--76/99+-61*17*62*12",
        "result": "-771480.2323232323"
    },
    {
        "exp": "26+-20/95/77*13+58+38*32",
        "result": "1299.9644565960355"
    },
    {
        "exp": "15*-35*11+48*-70/100--29*-58",
        "result": "-7490.6"
    },
    {
        "exp": "-70*-37*12/-61/30*-44+-15-25",
        "result": "707.2786885245903"
    },
    {
        "exp": "60-11+5-44+2+-12--99+-16",
        "result": "83"
    },
    {
        "exp": "79--98--71+81*76*46+66*-34",
        "result": "281180"
    },
    {
        "exp": "45--37+50/-5*-8-40/-25*-99",
        "result": "3.5999999999999943"
    },
    {
        "exp": "-30--79/-100-96*91/-21/33+-47",
        "result": "-65.1839393939394"
    },
    {
        "exp": "70+30--6*85*-87/-64*-50/-84",
        "result": "512.6674107142858"
    },
    {
        "exp": "92+19*25+-96+13*-50/47*3",
        "result": "429.51063829787233"
    },
    {
        "exp": "-6/-14--39+33--35+-1-99/-87",
        "result": "107.56650246305419"
    },
    {
        "exp": "65*-35+72+51--37*-71-53+-17",
        "result": "-4849"
    },
    {
        "exp": "32/11+68+47-37*57--85*45",
        "result": "1833.909090909091"
    },
    {
        "exp": "24+92+-62/18*-46+95*29*-73",
        "result": "-200840.55555555556"
    },
    {
        "exp": "3+28--54-59/39--42+-6+46",
        "result": "165.4871794871795"
    },
    {
        "exp": "33/89+75*-6--24/-3+32+38",
        "result": "-387.6292134831461"
    },
    {
        "exp": "85/-11+-34*42/24+86/63-100",
        "result": "-165.86219336219335"
    },
    {
        "exp": "25*41-7--85+-26/62-45-91",
        "result": "966.5806451612902"
    },
    {
        "exp": "42--19+61+30*-42*-85--75+16",
        "result": "107313"
    },
    {
        "exp": "-23+-34/24*18+25+14/2-1",
        "result": "-17.5"
    },
    {
        "exp": "-88*-27*7*-37*66*-41*-45-30",
        "result": "-74935309710"
    },
    {
        "exp": "98*56*-8--24+-33*-72-77*63",
        "result": "-46355"
    },
    {
        "exp": "93+12*22--83/-26/-58/83*21",
        "result": "357.013925729443"
    },
    {
        "exp": "25-2-16+84/98*65*72+-74",
        "result": "3944.428571428571"
    },
    {
        "exp": "-94/12/-45/2*-14/67/36/37",
        "result": "-1.3653786456439858e-05"
    },
    {
        "exp": "31/-46/70/-15+60*93/-2*-9",
        "result": "25110.000641821945"
    },
    {
        "exp": "(88)-(92*-93*(57))/(61/-(((-(-55+-46))))*-39)",
        "result": "20792.872635561158"
    },
    {
        "exp": "-(16)-(-27*-46+(24))-(-47+((((79*-82))))*-43)",
        "result": "-279789"
    },
    {
        "exp": "(2)+(41+-97--(53))*(-4/((((73+57))))*-42)",
        "result": "-1.8769230769230774"
    },
    {
        "exp": "(66)-(-27/23+(84))+(38*((((57--60))))*-90)",
        "result": "-400156.82608695654"
    },
    {
        "exp": "(72)*(-76+30/-(10))-(98/-((((59/43))))/1)",
        "result": "-5616.576271186441"
    },
    {
        "exp": "(59)/(-90/-64/-(73))+(-51+-(((-(98*-21))))+53)",
        "result": "-5118.7555555555555"
    },
    {
        "exp": "-(39)*(-73+-33-(92))/(75/-((((63+-19))))--87)",
        "result": "90.53237410071942"
    },
    {
        "exp": "-(49)-(66--55+-(32))+(63*-((((-9*-62))))-37)",
        "result": "-35329"
    },
    {
        "exp": "(83)+(35--40/-(95))+(23-((((54/-12))))*72)",
        "result": "464.57894736842104"
    },
    {
        "exp": "-(-6)+(-72+-17+-(40))*(87-(((-(79/-86))))/91)",
        "result": "-11215.697802197801"
    },
    {
        "exp": "(-30)*(77--43+-(27))*(35/-((((72/59))))+-23)",
        "result": "144188.75"
    },
    {
        "exp": "-(89)*(85+-28/(87))*(8/(((-(37*82))))--59)",
        "result": "-444625.15125133545"
    },
    {
        "exp": "-(-12)/(9+73/-(10))*(76*(((-(-70+-33))))+88)",
        "result": "55877.647058823524"
    },
    {
        "exp": "(-52)/(89/20*(64))*(90/((((56+-31))))/99)",
        "result": "-0.006639427987742594"
    },
    {
        "exp": "(75)*(78*-60+(63))+(64+-((((-93--11))))--72)",
        "result": "-346057"
    },
    {
        "exp": "-(-26)+(-6-14*(53))*(28--(((-(61/16))))*-26)",
        "result": "-95063.5"
    },
    {
        "exp": "-(-48)*(-64-6-(28))-(-31/((((-84/51))))+33)",
        "result": "-4755.821428571428"
    },
    {
        "exp": "(44)/(-47+6-(5))/(3/(((-(15-14))))+-47)",
        "result": "0.019130434782608695"
    },
    {
        "exp": "(67)*(-66--5/(4))+(49/-((((-86+32))))+6)",
        "result": "-4331.342592592592"
    },
    {
        "exp": "-(93)-(100/17--(13))+(89*-((((-91--45))))+-45)",
        "result": "3937.1176470588234"
    },
    {
        "exp": "-(-38)*(75/-62/(92))/(15--((((-46/8))))+98)",
        "result": "-0.0046587353740228914"
    },
    {
        "exp": "(-60)/(29*43*-(22))*(-14/((((82--3))))*-9)",
        "result": "0.0032420054119190874"
    },
    {
        "exp": "-(36)/(45*-46/-(90))*(-78*((((96/67))))*84)",
        "result": "14694.167423750812"
    },
    {
        "exp": "-(44)-(-87/-5--(24))-(-53--((((57*-74))))*-94)",
        "result": "-396524.4"
    },
    {
        "exp": "(-40)-(-93-39+-(18))-(91*((((-44/60))))-84)",
        "result": "260.73333333333335"
    },
    {
        "exp": "(-52)*(-19*42+(54))+(45/((((65*5))))+64)",
        "result": "38752.13846153846"
    },
    {
        "exp": "(-91)*(-65--33+-(58))/(-85*-((((-93*44))))*8)",
        "result": "-0.002943332758323271"
    },
    {
        "exp": "(52)+(-33*-90*-(40))*(-15/-(((-(-27--20))))*-54)",
        "result": "13746909.142857142"
    },
    {
        "exp": "-(-77)/(-33*-83+(91))*(70*-(((-(64-69))))*61)",
        "result": "-580.9010600706714"
    },
    {
        "exp": "(-33)-(58/92--(36))*(51/((((18/-26))))+34)",
        "result": "1420.0072463768117"
    },
    {
        "exp": "(-24)+(-4--49/(25))/(-29/-(((-(26/40))))+63)",
        "result": "-24.110962343096233"
    },
    {
        "exp": "-(95)/(40+98+-(13))/(-39+-((((-70+49))))/2)",
        "result": "0.02666666666666667"
    },
    {
        "exp": "(-90)-(71+-92*-(67))*(91/-(((-(30*-63))))-63)",
        "result": "393015.2037037037"
    },
    {
        "exp": "-(-58)/(-27*-55+(99))-(70*-((((-58/66))))+-24)",
        "result": "-37.47853535353536"
    },
    {
        "exp": "(-85)-(-15+88+-(10))+(-76+((((-39-16))))--65)",
        "result": "-214"
    },
    {
        "exp": "-(-17)-(-94+56--(23))-(26-(((-(-75/-93))))--71)",
        "result": "-65.80645161290323"
    },
    {
        "exp": "-(25)-(38+43-(80))/(31*(((-(-93+53))))*-14)",
        "result": "-24.999942396313365"
    },
    {
        "exp": "(46)-(-8*-66*(77))-(72--((((-77--38))))+-65)",
        "result": "-40578"
    },
    {
        "exp": "(5)+(54/83/(56))+(-36*(((-(80/70))))*-66)",
        "result": "-2710.416953528399"
    },
    {
        "exp": "(10)-(-35*50*(50))/(-87-((((-75+93))))--97)",
        "result": "-10927.5"
    },
    {
        "exp": "(-93)*(-69/22/(15))-(-38--(((-(-76/60))))+-68)",
        "result": "124.17878787878789"
    },
    {
        "exp": "(-15)/(-42*-80*-(85))+(95-((((-56*20))))*-7)",
        "result": "-7744.999947478992"
    },
    {
        "exp": "(-1)/(-75--12*(68))-(95-((((-38/-35))))+-48)",
        "result": "-45.91563524195103"
    },
    {
        "exp": "(23)/(56/37+(51))*(35--((((-100/-49))))--50)",
        "result": "38.122354448727506"
    },
    {
        "exp": "-(13)-(100--10*-(63))+(60*((((10--20))))+-19)",
        "result": "2298"
    },
    {
        "exp": "(63)-(-17+-79+(11))+(38--(((-(76--38))))*-27)",
        "result": "3264"
    },
    {
        "exp": "(-3)-(-65+68+(33))/(49*(((-(-23/-72))))/-64)",
        "result": "-150.19432120674358"
    },
    {
        "exp": "(-43)/(-17/95-(55))+(47+((((-49+50))))+-18)",
        "result": "30.779282716520413"
    },
    {
        "exp": "(-14)-(-96-50+-(84))-(-12*(((-(10-88))))*67)",
        "result": "62928"
    },
    {
        "exp": "(50)-(28+30+-(37))-(-72/(((-(-59/72))))*-48)",
        "result": "-4188.491525423729"
    },
    {
        "exp": "(60)-(-39*24-(6))+(40*(((-(-88*-1))))+-9)",
        "result": "-2527"
    },
    {
        "exp": "(20)+(-64-31--(40))+(-21/-((((16+6))))*90)",
        "result": "50.90909090909091"
    },
    {
        "exp": "(-86)*(-8--57*(49))*(85--((((67+21))))-46)",
        "result": "-30417770"
    },
    {
        "exp": "-(55)+(-20/9+-(75))/(-15-((((39--59))))--3)",
        "result": "-54.2979797979798"
    },
    {
        "exp": "(59)/(66/-64/-(10))-(56*-((((-69*-15))))*55)",
        "result": "3188372.121212121"
    },
    {
        "exp": "-(-44)*(86+15--(4))*(-55+((((-96/49))))*-84)",
        "result": "506219.99999999994"
    },
    {
        "exp": "(45)+(-74--93+-(5))*(40/((((4--45))))*51)",
        "result": "627.8571428571429"
    },
    {
        "exp": "-(-18)-(-27--87+(55))-(85/-(((-(-14+4))))-3)",
        "result": "-85.5"
    },
    {
        "exp": "(52)/(-22+-16+(40))-(33--(((-(67*-25))))-64)",
        "result": "-1618.0"
    },
    {
        "exp": "(-71)-(-95+-56/(50))*(61+(((-(-10*18))))*33)",
        "result": "576745.12"
    },
    {
        "exp": "-(-34)*(-96*-41+-(2))*(87/((((1-23))))-26)",
        "result": "-4006600.1818181816"
    },
    {
        "exp": "(29)-(58+14*-(2))/(52*(((-(95--20))))*-3)",
        "result": "28.998327759197323"
    },
    {
        "exp": "(-75)-(10+-98/-(30))-(89/-((((-90--33))))--11)",
        "result": "-100.8280701754386"
    },
    {
        "exp": "-(52)*(-9/-92+-(34))*(-90*-(((-(8--42))))+24)",
        "result": "-7890798.782608695"
    },
    {
        "exp": "(77)+(-55--12+-(14))+(47-(((-(9/-94))))+88)",
        "result": "154.90425531914894"
    },
    {
        "exp": "(95)*(24+-94/(92))*(48*-((((-83*-57))))+82)",
        "result": "-495539293.2608696"
    },
    {
        "exp": "-(90)-(-81*-57/(18))*(77+(((-(36+26))))/-60)",
        "result": "-20105.55"
    },
    {
        "exp": "-(67)+(-41+-69-(44))/(-79*(((-(1/66))))+71)",
        "result": "-69.13305351521511"
    },
    {
        "exp": "-(-95)+(85-71/-(39))/(75*(((-(68/15))))-47)",
        "result": "94.77565758961107"
    },
    {
        "exp": "(3)-(-27-6+-(27))+(-48/((((61/-33))))/73)",
        "result": "63.35571524814732"
    },
    {
        "exp": "-(31)/(-27/42+-(46))-(63*-(((-(-15+-95))))-57)",
        "result": "6987.664624808575"
    },
    {
        "exp": "-(81)-(-87/70/-(55))/(-32*(((-(-99+41))))+37)",
        "result": "-80.99998757701891"
    },
    {
        "exp": "(-44)-(33*-21--(34))/(29-((((15*53))))/-73)",
        "result": "-27.47973901098901"
    },
    {
        "exp": "(95)*(-43/72+-(80))*(-60+((((-84/-93))))*30)",
        "result": "251931.3172043011"
    },
    {
        "exp": "-(33)/(-73*24/(1))+(-82--(((-(57--88))))*33)",
        "result": "-4866.981164383562"
    },
    {
        "exp": "-(-16)+(64*-43/-(93))-(-29/(((-(30*-62))))*85)",
        "result": "46.91666666666667"
    },
    {
        "exp": "-(-6)*(-76/-98+(17))*(62/((((-28-12))))/88)",
        "result": "-1.878548237476809"
    },
    {
        "exp": "-(27)/(-76-97*(22))+(47*((((16*83))))-39)",
        "result": "62377.01221719457"
    },
    {
        "exp": "(88)/(24*-98+(17))+(-67+((((15/-10))))/-21)",
        "result": "-66.96625879473845"
    },
    {
        "exp": "(26)+(6/-78*-(39))-(-8+(((-(-26*47))))*-88)",
        "result": "107573.0"
    },
    {
        "exp": "(-21)-(14+7/(68))/(56*((((88/51))))--73)",
        "result": "-21.08314067737834"
    },
    {
        "exp": "(38)+(-3+61*-(69))/(-49-(((-(-57+-6))))*66)",
        "result": "39.001188495364865"
    },
    {
        "exp": "-(87)+(-18-57*-(72))*(100*(((-(-33--19))))*42)",
        "result": "240256713"
    },
    {
        "exp": "-(-27)-(-38+7/-(67))/(86-(((-(40*-1))))/-46)",
        "result": "27.438640132669985"
    },
    {
        "exp": "-(12)+(-38*-8*(4))-(18*((((-34*-56))))-7)",
        "result": "-33061"
    },
    {
        "exp": "(78)-(7-76+(32))-(87*(((-(11+89))))+98)",
        "result": "8717"
    },
    {
        "exp": "(-59)+(-33--25/(6))+(55--(((-(64-44))))-5)",
        "result": "-57.83333333333333"
    },
    {
        "exp": "-(15)-(18+88*(38))+(-25/((((23+84))))*-42)",
        "result": "-3367.1869158878503"
    },
    {
        "exp": "(15)+(-25/-66*(42))*(47+((((-57-31))))/88)",
        "result": "746.8181818181818"
    },
    {
        "exp": "(51)/(1/-86*(55))*(-37+-(((-(15-35))))-94)",
        "result": "12041.563636363635"
    },
    {
        "exp": "-(86)*(-6--44-(67))+(-3/-(((-(11+-81))))/-100)",
        "result": "2493.9995714285715"
    },
    {
        "exp": "(67)/(-44/-44+(25))/(-8/-(((-(-30*60))))/-49)",
        "result": "-28410.576923076926"
    },
    {
        "exp": "-(-93)+(-6/-66/-(17))*(-81*((((7/-13))))--50)",
        "result": "92.49938296997121"
    },
    {
        "exp": "(24)+(-17*74+-(58))+(93*-((((-81*96))))/7)",
        "result": "102017.71428571429"
    },
    {
        "exp": "-(-47)/(81/-51-(56))-(74+((((-28+14))))*-87)",
        "result": "-1292.8161389172626"
    },
    {
        "exp": "(-29)+(-41--72+(23))*(-11+((((7+-82))))--89)",
        "result": "133"
    },
    {
        "exp": "(-55)+(63*-42*(98))-(49*-((((-99/-38))))*41)",
        "result": "-254129.02631578947"
    },
    {
        "exp": "-(-17)*(88+-35/-(62))*(-7*-((((21*-79))))*-57)",
        "result": "996616234.3064516"
    },
    {
        "exp": "-(96)/(-43--20/(1))/(-90/-((((44+-83))))+-76)",
        "result": "-0.05330144358076364"
    },
    {
        "exp": "(-31)-(78+-36/-(86))+(-18--((((-56-48))))+40)",
        "result": "-191.4186046511628"
    },
    {
        "exp": "-16-27-30-80",
        "result": "-153"
    },
    {
        "exp": "-88--46-46-5",
        "result": "-93"
    },
    {
        "exp": "-27--55--4-19",
        "result": "13"
    },
    {
        "exp": "81-49--39-92",
        "result": "-21"
    },
    {
        "exp": "70-10--86-86",
        "result": "60"
    },
    {
        "exp": "-66--37-72-88",
        "result": "-189"
    },
    {
        "exp": "45-41-13-80",
        "result": "-89"
    },
    {
        "exp": "60-67--27--7",
        "result": "27"
    },
    {
        "exp": "11-84--33--7",
        "result": "-33"
    },
    {
        "exp": "-100-87--27-63",
        "result": "-223"
    },
    {
        "exp": "4-90--9-56",
        "result": "-133"
    },
    {
        "exp": "-59-70--31--96",
        "result": "-2"
    },
    {
        "exp": "75--99-43-76",
        "result": "55"
    },
    {
        "exp": "79--52-5-21",
        "result": "105"
    },
    {
        "exp": "55--15--85-27",
        "result": "128"
    },
    {
        "exp": "29--40--77-31",
        "result": "115"
    },
    {
        "exp": "74-21--11--92",
        "result": "156"
    },
    {
        "exp": "-68--3--10-70",
        "result": "-125"
    },
    {
        "exp": "1-41--6-89",
        "result": "-123"
    },
    {
        "exp": "-53-93--65--99",
        "result": "18"
    },
    {
        "exp": "-38-72--21--94",
        "result": "5"
    },
    {
        "exp": "22-51--54-15",
        "result": "10"
    },
    {
        "exp": "40--45-13-94",
        "result": "-22"
    },
    {
        "exp": "78-77-37-70",
        "result": "-106"
    },
    {
        "exp": "-50--7-60-5",
        "result": "-108"
    },
    {
        "exp": "41--86--75--45",
        "result": "247"
    },
    {
        "exp": "-75-97-12-34",
        "result": "-218"
    },
    {
        "exp": "24-29--37-21",
        "result": "11"
    },
    {
        "exp": "59-2--72--15",
        "result": "144"
    },
    {
        "exp": "15--6-72--81",
        "result": "30"
    },
    {
        "exp": "-24--43-93-99",
        "result": "-173"
    },
    {
        "exp": "33--28--100-1",
        "result": "160"
    },
    {
        "exp": "-55-54-80-59",
        "result": "-248"
    },
    {
        "exp": "76-70--87-61",
        "result": "32"
    },
    {
        "exp": "-83--93-92-100",
        "result": "-182"
    },
    {
        "exp": "90-77-23--98",
        "result": "88"
    },
    {
        "exp": "-97--30-59--57",
        "result": "-69"
    },
    {
        "exp": "-5-3--30-8",
        "result": "14"
    },
    {
        "exp": "50-14--49--42",
        "result": "127"
    },
    {
        "exp": "96-15-1-85",
        "result": "-5"
    },
    {
        "exp": "-20-67--84--67",
        "result": "64"
    },
    {
        "exp": "-68--57--65-29",
        "result": "25"
    },
    {
        "exp": "-73--76-6--14",
        "result": "11"
    },
    {
        "exp": "-6-79-83--76",
        "result": "-92"
    },
    {
        "exp": "24--84--98-43",
        "result": "163"
    },
    {
        "exp": "63--30-83--85",
        "result": "95"
    },
    {
        "exp": "-19-39--61-92",
        "result": "-89"
    },
    {
        "exp": "-9-25-75--36",
        "result": "-73"
    },
    {
        "exp": "23-94-62--90",
        "result": "-43"
    },
    {
        "exp": "-12-2-78-50",
        "result": "-142"
    },
    {
        "exp": "-82-20-54-42",
        "result": "-198"
    },
    {
        "exp": "-85--62-1-68",
        "result": "-92"
    },
    {
        "exp": "-56-61-77--38",
        "result": "-156"
    },
    {
        "exp": "-39--36--60--24",
        "result": "81"
    },
    {
        "exp": "-2--65-99-36",
        "result": "-72"
    },
    {
        "exp": "-95--100--48--1",
        "result": "54"
    },
    {
        "exp": "-93--16--44-65",
        "result": "-98"
    },
    {
        "exp": "-47-43--22--79",
        "result": "11"
    },
    {
        "exp": "36--74--20--67",
        "result": "197"
    },
    {
        "exp": "-55--89-4--50",
        "result": "80"
    },
    {
        "exp": "-50--21--23--9",
        "result": "3"
    },
    {
        "exp": "52--83-2-1",
        "result": "132"
    },
    {
        "exp": "-93-39-73-8",
        "result": "-213"
    },
    {
        "exp": "-43--34-78-92",
        "result": "-179"
    },
    {
        "exp": "-44-48--46--66",
        "result": "20"
    },
    {
        "exp": "77-8-7--84",
        "result": "146"
    },
    {
        "exp": "10--91--6-67",
        "result": "40"
    },
    {
        "exp": "-26-18--64-40",
        "result": "-20"
    },
    {
        "exp": "23-74--72-20",
        "result": "1"
    },
    {
        "exp": "71-57-36--93",
        "result": "71"
    },
    {
        "exp": "-99-50-49--78",
        "result": "-120"
    },
    {
        "exp": "78--67-80--27",
        "result": "92"
    },
    {
        "exp": "7-30--39-44",
        "result": "-28"
    },
    {
        "exp": "-23-27-93-71",
        "result": "-214"
    },
    {
        "exp": "100--99--45--51",
        "result": "295"
    },
    {
        "exp": "100--96-92-99",
        "result": "5"
    },
    {
        "exp": "93-28-70-9",
        "result": "-14"
    },
    {
        "exp": "-9-68-53-47",
        "result": "-177"
    },
    {
        "exp": "-65-15--70--20",
        "result": "10"
    },
    {
        "exp": "-58--22-87-66",
        "result": "-189"
    },
    {
        "exp": "61--3-48--43",
        "result": "59"
    },
    {
        "exp": "-75-20-4--28",
        "result": "-71"
    },
    {
        "exp": "15--77--2-77",
        "result": "17"
    },
    {
        "exp": "-20--11-11-83",
        "result": "-103"
    },
    {
        "exp": "80--5-25-53",
        "result": "7"
    },
    {
        "exp": "60--94-46-72",
        "result": "36"
    },
    {
        "exp": "-54-27--44-91",
        "result": "-128"
    },
    {
        "exp": "31--27--83--100",
        "result": "241"
    },
    {
        "exp": "84-28-65-41",
        "result": "-50"
    },
    {
        "exp": "38-54--90-5",
        "result": "69"
    },
    {
        "exp": "-71--38--18--85",
        "result": "70"
    },
    {
        "exp": "-27-41-85-37",
        "result": "-190"
    },
    {
        "exp": "-20-49--6-49",
        "result": "-112"
    },
    {
        "exp": "9-92-25-13",
        "result": "-121"
    },
    {
        "exp": "-51-7--38--99",
        "result": "79"
    },
    {
        "exp": "-36-42-58-90",
        "result": "-226"
    },
    {
        "exp": "-56--76-92--99",
        "result": "27"
    },
    {
        "exp": "-38--92--24-7",
        "result": "71"
    },
    {
        "exp": "55-47-55-88",
        "result": "-135"
    },
    {
        "exp": "77-88--44--31",
        "result": "64"
    }
]

# print(calc('(67)/(-44/-44+(25))/(-8/-(((-(-30*60))))/-49)'))

for i, t in enumerate(tests):
    if calc(t['exp']) != float(t['result']):
        print(t['exp'])
        print(calc(t['exp']))
        print(t['result'])
