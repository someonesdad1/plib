'''

ToDo
    - Write an access function that uses the data to linearly interpolate
      to the user's wavelength.
    - Compare the approximation to the interpolated table values.  Print
      out % deviations.
    - In the cie_cmf_analytical_code.zip file,
      xyzViewer/data/intraObserverVariance_20nm.h gives data on the
      variance at various wavelengths.  Use interpolation for these numbers
      to estimate the standard deviation of the diffs and display them as
      nominal normal deviates.


From 204.xls downloaded from
https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
Thu 24 Mar 2022
'''
from pdb import set_trace as xx 
from wrap import dedent
from math import exp

# This table is the standard method to convert from a power spectral
# density (PSD) function to X, Y, Z tristimulus coordinates.  The PSD is
# integrated with these numerical functions over the wavelengths of 380 to
# 780 nm.  These are for the 2° field of view.  The table below this one is
# for the 1964 10° field of view.  These numbers were derived around 1930
# from two experimental samples from 17 people.  The experiments were
# careful and have been repeated, so though the samples were clearly
# biased, it seems they represent a large portion of humanity.

data1 = '''
# CIE 1931 standard colorimetric observer			
# Columns: 
#     wavelength, nm
#     xbar(wl_nm)
#     ybar(wl_nm)
#     zbar(wl_nm)
380	0.001368	0.000039	0.006450
385	0.002236	0.000064	0.010550
390	0.004243	0.000120	0.020050
395	0.007650	0.000217	0.036210
400	0.014310	0.000396	0.067850
405	0.023190	0.000640	0.110200
410	0.043510	0.001210	0.207400
415	0.077630	0.002180	0.371300
420	0.134380	0.004000	0.645600
425	0.214770	0.007300	1.039050
430	0.283900	0.011600	1.385600
435	0.328500	0.016840	1.622960
440	0.348280	0.023000	1.747060
445	0.348060	0.029800	1.782600
450	0.336200	0.038000	1.772110
455	0.318700	0.048000	1.744100
460	0.290800	0.060000	1.669200
465	0.251100	0.073900	1.528100
470	0.195360	0.090980	1.287640
475	0.142100	0.112600	1.041900
480	0.095640	0.139020	0.812950
485	0.057950	0.169300	0.616200
490	0.032010	0.208020	0.465180
495	0.014700	0.258600	0.353300
500	0.004900	0.323000	0.272000
505	0.002400	0.407300	0.212300
510	0.009300	0.503000	0.158200
515	0.029100	0.608200	0.111700
520	0.063270	0.710000	0.078250
525	0.109600	0.793200	0.057250
530	0.165500	0.862000	0.042160
535	0.225750	0.914850	0.029840
540	0.290400	0.954000	0.020300
545	0.359700	0.980300	0.013400
550	0.433450	0.994950	0.008750
555	0.512050	1.000000	0.005750
560	0.594500	0.995000	0.003900
565	0.678400	0.978600	0.002750
570	0.762100	0.952000	0.002100
575	0.842500	0.915400	0.001800
580	0.916300	0.870000	0.001650
585	0.978600	0.816300	0.001400
590	1.026300	0.757000	0.001100
595	1.056700	0.694900	0.001000
600	1.062200	0.631000	0.000800
605	1.045600	0.566800	0.000600
610	1.002600	0.503000	0.000340
615	0.938400	0.441200	0.000240
620	0.854450	0.381000	0.000190
625	0.751400	0.321000	0.000100
630	0.642400	0.265000	0.000050
635	0.541900	0.217000	0.000030
640	0.447900	0.175000	0.000020
645	0.360800	0.138200	0.000010
650	0.283500	0.107000	0.000000
655	0.218700	0.081600	0.000000
660	0.164900	0.061000	0.000000
665	0.121200	0.044580	0.000000
670	0.087400	0.032000	0.000000
675	0.063600	0.023200	0.000000
680	0.046770	0.017000	0.000000
685	0.032900	0.011920	0.000000
690	0.022700	0.008210	0.000000
695	0.015840	0.005723	0.000000
700	0.011359	0.004102	0.000000
705	0.008111	0.002929	0.000000
710	0.005790	0.002091	0.000000
715	0.004109	0.001484	0.000000
720	0.002899	0.001047	0.000000
725	0.002049	0.000740	0.000000
730	0.001440	0.000520	0.000000
735	0.001000	0.000361	0.000000
740	0.000690	0.000249	0.000000
745	0.000476	0.000172	0.000000
750	0.000332	0.000120	0.000000
755	0.000235	0.000085	0.000000
760	0.000166	0.000060	0.000000
765	0.000117	0.000042	0.000000
770	0.000083	0.000030	0.000000
775	0.000059	0.000021	0.000000
780	0.000042	0.000015	0.000000
!Sum:21.371524	21.371327	21.371540
'''[1:-1]

data2 = '''
# CIE 1964 supplementary standard colorimetric observer			
# Columns: 
#     wavelength, nm
#     xbar10(wl_nm)
#     ybar10(wl_nm)
#     zbar10(wl_nm)
# 
380	0.000160	0.000017	0.000705
385	0.000662	0.000072	0.002928
390	0.002362	0.000253	0.010482
395	0.007242	0.000769	0.032344
400	0.019110	0.002004	0.086011
405	0.043400	0.004509	0.197120
410	0.084736	0.008756	0.389366
415	0.140638	0.014456	0.656760
420	0.204492	0.021391	0.972542
425	0.264737	0.029497	1.282500
430	0.314679	0.038676	1.553480
435	0.357719	0.049602	1.798500
440	0.383734	0.062077	1.967280
445	0.386726	0.074704	2.027300
450	0.370702	0.089456	1.994800
455	0.342957	0.106256	1.900700
460	0.302273	0.128201	1.745370
465	0.254085	0.152761	1.554900
470	0.195618	0.185190	1.317560
475	0.132349	0.219940	1.030200
480	0.080507	0.253589	0.772125
485	0.041072	0.297665	0.570060
490	0.016172	0.339133	0.415254
495	0.005132	0.395379	0.302356
500	0.003816	0.460777	0.218502
505	0.015444	0.531360	0.159249
510	0.037465	0.606741	0.112044
515	0.071358	0.685660	0.082248
520	0.117749	0.761757	0.060709
525	0.172953	0.823330	0.043050
530	0.236491	0.875211	0.030451
535	0.304213	0.923810	0.020584
540	0.376772	0.961988	0.013676
545	0.451584	0.982200	0.007918
550	0.529826	0.991761	0.003988
555	0.616053	0.999110	0.001091
560	0.705224	0.997340	0.000000
565	0.793832	0.982380	0.000000
570	0.878655	0.955552	0.000000
575	0.951162	0.915175	0.000000
580	1.014160	0.868934	0.000000
585	1.074300	0.825623	0.000000
590	1.118520	0.777405	0.000000
595	1.134300	0.720353	0.000000
600	1.123990	0.658341	0.000000
605	1.089100	0.593878	0.000000
610	1.030480	0.527963	0.000000
615	0.950740	0.461834	0.000000
620	0.856297	0.398057	0.000000
625	0.754930	0.339554	0.000000
630	0.647467	0.283493	0.000000
635	0.535110	0.228254	0.000000
640	0.431567	0.179828	0.000000
645	0.343690	0.140211	0.000000
650	0.268329	0.107633	0.000000
655	0.204300	0.081187	0.000000
660	0.152568	0.060281	0.000000
665	0.112210	0.044096	0.000000
670	0.081261	0.031800	0.000000
675	0.057930	0.022602	0.000000
680	0.040851	0.015905	0.000000
685	0.028623	0.011130	0.000000
690	0.019941	0.007749	0.000000
695	0.013842	0.005375	0.000000
700	0.009577	0.003718	0.000000
705	0.006605	0.002565	0.000000
710	0.004553	0.001768	0.000000
715	0.003145	0.001222	0.000000
720	0.002175	0.000846	0.000000
725	0.001506	0.000586	0.000000
730	0.001045	0.000407	0.000000
735	0.000727	0.000284	0.000000
740	0.000508	0.000199	0.000000
745	0.000356	0.000140	0.000000
750	0.000251	0.000098	0.000000
755	0.000178	0.000070	0.000000
760	0.000126	0.000050	0.000000
765	0.000090	0.000036	0.000000
770	0.000065	0.000025	0.000000
775	0.000046	0.000018	0.000000
780	0.000033	0.000013	0.000000
!Sum:23.329353	23.332036	23.334153
'''[1:-1]
indent = " "*4
def CIE_Data(dbg=False):
    tab = "\t"
    def GetData(data):
        f = lambda x: float(x)
        out = []
        for line in data.split("\n"):
            if line[0] == "#":
                continue
            if line[0] == "!":
                sums = [f(i) for i in line[5:].split(tab)]
                continue
            s = line.split(tab)
            nm = int(s[0])
            r = [f(i) for i in s[1:]]
            out.append((nm, r))
        # Check sums
        x, y, z = 0, 0, 0
        for nm, r in out:
            x += r[0]
            y += r[1]
            z += r[2]
        g = lambda x: round(x, 6)
        if g(x) != sums[0]:
            print("Error:  bad x sum")
            print(x, sums[0])
            exit(1)
        if g(y) != sums[1]:
            print("Error:  bad y sum")
            print(y, sums[1])
            exit(1)
        if g(z) != sums[2]:
            print("Error:  bad z sum")
            print(z, sums[2])
            exit(1)
        return out
    def Header():
        print(dedent(f'''
        # Raw data data from
        # https://web.archive.org/web/20170131100357/http://files.cie.co.at/204.xls
        # Downloaded 24 Mar 2022
 
        '''))
    def Output(out, suppl=False):
        if suppl:
            print(dedent(f'''
            # CIE 1964 supplementary standard colorimetric observer			
            # Structure:  (wavelength_nm, (xbar10, ybar10, zbar10))
            # Columns: 
            #     wavelength, nm
            #     xbar10(wl_nm), dimensionless
            #     ybar10(wl_nm), dimensionless
            #     zbar10(wl_nm), dimensionless
    
            CIE1964_suppl_CMF = (
            '''))
        else:
            print(dedent(f'''
            # CIE 1931 standard colorimetric observer			
            # Structure:  (wavelength_nm, (xbar, ybar, zbar))
            # Columns: 
            #     wavelength, nm
            #     xbar(wl_nm), dimensionless
            #     ybar(wl_nm), dimensionless
            #     zbar(wl_nm), dimensionless
    
            CIE1931_CMF = (
            '''))
        i = indent
        if dbg:
            out = out[:10]
        for wl, xyz in out:
            x, y, z = xyz
            print(f"{i}({wl:3d}, ({x:8.6f}, {y:8.6f}, {z:8.6f})),")
        print(f")")
        if suppl:
            print()
    Header()
    out = GetData(data2)
    Output(out, suppl=True)
    out = GetData(data1)
    Output(out)
def CIE_CMF_Approx(nm):
    '''Produce the CIE 1931 CMFs with piecewise-linear approximations.  From
    C. Wyman, et. al., "Simple Analytic Approximations to the CIE XYZ Color
    Matching Functions", Journal of Computer Graphics Techniques, vol. 2,
    no. 2, 2013.  https://jcgt.org/published/0002/02/01/
    '''
    if not (380 <= nm <= 780):
        raise ValueError(f"'{nm}' must be between 380 and 780 nm")
    T = lambda boolean, a, b: a if boolean else b
    t1 = (nm - 442)*T(nm < 442, 0.0624, 0.0374)
    t2 = (nm - 599.8)*T(nm < 599.8, 0.0264, 0.0323)
    t3 = (nm - 501.1)*T(nm < 501.1, 0.049, 0.0382)
    x = 0.362*exp(-t1**2/2) + 1.056*exp(-t2**2/2) - 0.065*exp(-t3**2/2)
    t1 = (nm - 568.8)*T(nm < 568.8, 0.0213, 0.0247)
    t2 = (nm - 530.9)*T(nm < 530.9, 0.0613, 0.0322)
    y = 0.821*exp(-t1**2/2) + 0.286*exp(-t2**2/2)
    t1 = (nm - 437)*T(nm < 437, 0.0845, 0.0278)
    t2 = (nm - 459)*T(nm < 459, 0.0385, 0.0725)
    z = 1.217*exp(-t1**2/2) + 0.681*exp(-t2**2/2)
    return x, y, z
def CIE_CMF_Approximation(dbg=False, nm_step=5):
    i = indent
    if dbg:
        nm_step = 30
    print(dedent(f'''
    # Analytical approximation to CIE 1931 CMF\n
    CIE1931_CMF = (
    '''))
    for nm in range(380, 781, nm_step):
        x, y, z = CIE_CMF_Approx(nm)
        print(f"{i}({nm:3d}, ({x:8.6f}, {y:8.6f}, {z:8.6f})),")

if __name__ == "__main__": 
    dbg = 0
    if 1:
        CIE_Data(dbg=dbg)
    CIE_CMF_Approximation(dbg=dbg)
