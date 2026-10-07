"""Reutiliza los valores ya calculados y evalúa E3 y controles posteriores.

No cambia fuentes/PDF; todas las escrituras son locales a este directorio.
No abre los campos externos de las tablas hasta después de calcular cada masa.
No convierte coincidencia decimal, firma leída o PASS en prueba de procedencia.
"""
import argparse
import csv
from decimal import Decimal as D, localcontext
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
PACKAGE = AUDIT / 'DEPENDENCIAS/CORPUS_2249'
BASE = PACKAGE / '00_BASE_SELLADA/01_FUENTE_SUCESORA'
PREVIOUS = AUDIT / 'VALORES_RECALCULADOS_CORPUS.json'
COMPOUNDS = BASE / 'datos/masas_rev_acumulativa/fuentes/refinamiento_compuestos_e3_beta_rev3.tsv'
PUBLIC = BASE / 'datos/masas_rev_acumulativa/salidas/tabla_comparativa_masas_publica.tsv'
NIST = 'https://physics.nist.gov/cuu/Constants/ArchiveASCII/allascii_2018.txt'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sin(x):
    t = s = x
    k = 1
    while abs(t) > D('1e-90'):
        t *= -x*x / ((2*k)*(2*k+1))
        s += t
        k += 1
    return s

def cos(x):
    t = s = D(1)
    k = 1
    while abs(t) > D('1e-90'):
        t *= -x*x / ((2*k-1)*(2*k))
        s += t
        k += 1
    return s

def build():
    old = json.loads(PREVIOUS.read_text())
    with localcontext() as ctx:
        ctx.prec = 90
        v = {r['nombre']:D(r['valor']) for r in old['valores']}
        pi, alpha = v['pi_HMT'],v['alpha_12']
        x,y = pi*v['A_grados']/180,pi*v['C_estrella_grados']/180
        me,delta = v['electron_beta_MeV'],v['Delta4']
        s120 = v['torre_s_120']
        z270 = 135*delta**2
        e3 = []
        def mass_e3(name,signature):
            na,sc,k,n120,n270 = map(D,signature)
            value=me*(na*x+sc*y/6+k*delta+n120*s120+n270*z270).exp()
            record={'estado':name,'firma':list(signature),'MeV_c2':str(value),
                    'formula':'m_e_beta exp(n_A*x+s_C*y/6+k*Delta4+nu120*s120+nu270*135*Delta4^2)',
                    'alcance':'evaluacion de la firma E3 publicada; no se infiere su selector prospectivo del ajuste'}
            e3.append(record)
            return value,record
        for name,sig in [('mu',(42,-3,8,0,2)),('tau',(64,0,25,-1,6)),
                         ('W',(94,-1,0,-2,4)),('Z',(95,-1,-11,0,-4))]:
            mass_e3(name,sig)
        with COMPOUNDS.open(encoding='utf8',newline='') as f:
            for row in csv.DictReader(f,delimiter='\t'):
                sig=tuple(int(row[k]) for k in ('n_A','s_C','k_Delta4','nu120','nu270'))
                value,record=mass_e3(row['display_name'],sig)
                # Comparación sólo después de evaluar la firma.
                printed=D(row['mass_E3_beta_MeV'])
                record['residual_con_impreso_MeV']=str(value-printed)
                # Las fuentes mezclan precisiones de los antecedentes. Se exige
                # reproducir las 24 cifras decimales mostradas, no identidad de
                # los 100 dígitos de un fichero calculado con otros truncamientos.
                require(abs(value-printed)<D('1e-24'),'E3 no reproduce el prefijo publicado: '+row['display_name'])
                record['control_impreso']='diferencia absoluta menor que 1e-24 MeV; no igualdad de todos los digitos del fichero'
                record['selector_de_firma_segun_tabla']=row['assignment_status']
        require(len(e3)==10,'No se recuperaron diez evaluaciones E3')

        # Matriz compleja CKM en la parametrización escrita, con C=R^2.
        ang=[pi*v['CKM_'+key+'_grados']/180 for key in ('theta12','theta23','theta13','delta_CP')]
        a,b,c,d=ang
        c12,c23,c13=cos(a),cos(b),cos(c)
        s12,s23,s13=sin(a),sin(b),sin(c)
        cd,sd=cos(d),sin(d)
        z=lambda re,im=0:(D(re),D(im))
        V=[[z(c12*c13),z(s12*c13),z(s13*cd,-s13*sd)],
           [z(-s12*c23-c12*s23*s13*cd,-c12*s23*s13*sd),
            z(c12*c23-s12*s23*s13*cd,-s12*s23*s13*sd),z(s23*c13)],
           [z(s12*s23-c12*c23*s13*cd,-c12*c23*s13*sd),
            z(-c12*s23-s12*c23*s13*cd,-s12*c23*s13*sd),z(c23*c13)]]
        defects=[]
        for i in range(3):
            for j in range(3):
                re=sum(V[k][i][0]*V[k][j][0]+V[k][i][1]*V[k][j][1] for k in range(3))-D(i==j)
                im=sum(V[k][i][0]*V[k][j][1]-V[k][i][1]*V[k][j][0] for k in range(3))
                defects.extend((abs(re),abs(im)))
        require(max(defects)<D('1e-85'),'Defecto numérico CKM excesivo')
        M=[[Q(2),Q(-5),Q(28)],[Q(0),Q(7),Q(-25,2)],[Q(1),Q(-20),Q(-2,3)]]
        det=sum(M[0][j]*(M[1][(j+1)%3]*M[2][(j+2)%3]-M[1][(j+2)%3]*M[2][(j+1)%3]) for j in range(3))
        require(det==Q(-3857,6),'Determinante racional CKM')
        gamma=v['Barbero_Immirzi']
        weight_pole=Q(12,270)-Q(1,360)
        require(weight_pole==Q(1,24),'Polo de la cadena 12:-1')
        qm,qp=v['q_menos'],v['q_mas']
        lambert=lambda q,m:q**m/(1-q**(3*m))
        ds90=lambert(qm,90)-lambert(qp,90)
        ds120=lambert(qm,120)-lambert(qp,120)
        require(abs(gamma-(pi*v['A_grados']*v['C_estrella_grados']/180+12*ds90-ds120))<D('1e-85'),'Barbero')
        theta=v['theta_108']
        normalized_planck={
          'lP/l0':theta.sqrt(),'tP/t0':theta.sqrt(),
          'EP/(hbar/t0)':1/theta.sqrt(),'mP/(hbar/(c^2*t0))':1/theta.sqrt(),
          'FP/(hbar/(c*t0^2))':1/theta,'PP/(hbar/t0^2)':1/theta,
          'rhoP/(hbar/(c^5*t0^4))':1/theta**2,
          'area_Planck/l0^2':theta,
          'Gpre/Gret':1/v['R_act'],
          'area_minima_spin_medio/lP^2':4*pi*D(3).sqrt()*gamma}
        # Carta decimal publicada: evaluación, no búsqueda de sus cinco datos.
        gchart=Q(1,10**11)*(6+Q(674,1000)+Q(30,10**5))
        with PUBLIC.open(encoding='utf8',newline='') as f:
            classes=[{'clase':r['clase_y_representantes'],'salida_publicada':r['panel_b_salida_interna'],
                      'alcance':'transcripcion de inventario, no calculo nuevo'} for r in csv.DictReader(f,delimiter='\t')]
        require(len(classes)==23,'Inventario distinto de 23')

        # El comparador solicitado es 2018. No se usa para calcular anteriores.
        references={
          'electron_beta_MeV':('0.51099895000','0.00000000015','misma carta de energía; incertidumbre experimental solamente'),
          'h_pre_en_U_S':('6.62607015e-34','0','sólo después de identificar U_S con J s; definición SI exacta'),
          'h_ret_en_U_S':('6.62607015e-34','0','otra sección de acción; no confundir con pre'),
          'anomalia_muon':('0.00116592089','0.00000000063','funcional publicado de tres términos'),
          'Fermi_arbol_GeV_menos2':('0.000011663787','0.000000000006','árbol frente a renormalizado: diferencia descriptiva, no contraste homogéneo')}
        comparisons=[]
        for key,(ref,unc,note) in references.items():
            r,u=D(ref),D(unc)
            diff=v[key]-r
            comparisons.append({'objeto':key,'calculado':str(v[key]),'CODATA2018':ref,
                                'incertidumbre_estandar':unc,'diferencia':str(diff),
                                'diferencia_relativa':str(diff/r),
                                'diferencia_sobre_u_experimental':str(diff/u) if u and not key.startswith('Fermi') else None,
                                'condicion_de_comparabilidad':note})
        e3map={r['estado']:D(r['MeV_c2']) for r in e3}
        for name,ref,u in [('mu','105.6583755','0.0000023'),
                           ('proton','938.27208816','0.00000029'),('neutron','939.56542052','0.00000054')]:
            diff=e3map[name]-D(ref)
            comparisons.append({'objeto':'E3_'+name,'calculado':str(e3map[name]),'CODATA2018':ref,
                                'incertidumbre_estandar':u,'diferencia':str(diff),
                                'diferencia_relativa':str(diff/D(ref)),
                                'diferencia_sobre_u_experimental':str(diff/D(u)),
                                'condicion_de_comparabilidad':'firma E3 declarada; no incertidumbre teórica asignada'})
        return {'edicion_pdf_sha256':old['pdf_sha256'],'CODATA2018_fuente':NIST,
          'precedentes_reutilizados':str(PREVIOUS),'valores_previos':old['valores_recalculados'],
          'fuentes_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (PREVIOUS,COMPOUNDS,PUBLIC)},
          'E3':e3,'z270':str(z270),
          'CKM':{'modulos':[[str((re*re+im*im).sqrt()) for re,im in row] for row in V],
                 'defecto_unitariedad_maximo':str(max(defects)),'det_M_racional':str(det)},
          'Barbero':{'DeltaS90':str(ds90),'DeltaS120':str(ds120),'peso':[12,-1],
                     'polo_exacto':str(weight_pole),'gamma':str(gamma),
                     'procedencia':'cadena fundamental doce sectores y una costura; ecuacion diofantica posterior'},
          'Planck_relaciones_normalizadas':{k:str(w) for k,w in normalized_planck.items()},
          'G_carta_decimal':{'racional':str(gchart),'decimal':str(D(gchart.numerator)/D(gchart.denominator)),
                            'antecedentes_de_carta':[11,6,5,674,30],
                            'alcance':'se evalua la carta publicada; no equivale a evaluar G_hol'},
          'comparaciones_CODATA2018':comparisons,'clases_publicadas_23':classes,
          'alcance':'evaluaciones y controles del bloque MASAS, no certificacion global de todas las identificaciones fisicas'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-report',action='store_true')
    args=parser.parse_args()
    result=build()
    payload=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.write_report:
        (HERE/'CALCULOS_COMPLEMENTARIOS.json').write_text(payload,encoding='utf8')
    print(json.dumps({'E3_calculadas':len(result['E3']),
                      'CKM_defecto':result['CKM']['defecto_unitariedad_maximo'],
                      'sha256_resultado':hashlib.sha256(payload.encode()).hexdigest()},indent=2))
