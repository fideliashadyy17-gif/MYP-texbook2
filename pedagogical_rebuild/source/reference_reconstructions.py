"""Coursebook-style reconstructions derived from the mathematical content of supplied exams.
Administrative headers, school branding, candidate instructions and exam page furniture are excluded.
"""
REFERENCE_PRACTICE = {
(2,1): {"source":"MYP2 Term 1 papers A/B","title":"Source-informed practice · Ratio", "tasks":[
("FOUNDATION","Simplify 750 m : 2 km. Show the unit conversion before simplifying."),
("APPLICATION","Afi and Kossi share 3,600 FCFA in the ratio 5:4. Find each share and check that the shares total 3,600 FCFA."),
("REASONING","The ratio of boys to girls in a choir is 4:5. There are 12 more girls than boys. Determine the number of boys, girls and total singers."),
("PROBLEM SOLVING","Paint colours are mixed in the ratio red:blue:white = 3:4:1. Calculate the volume of each colour needed for 20 litres of paint.")],"answers":["3:8.","2,000 FCFA and 1,600 FCFA.","48 boys, 60 girls; 108 singers.","7.5 L red, 10 L blue, 2.5 L white."]},
(2,2): {"source":"MYP2 Term 1 papers A/B","title":"Source-informed practice · Direct proportion", "tasks":[
("FOUNDATION","y is directly proportional to x and y=15 when x=6. Find k in y=kx and calculate y when x=14."),
("APPLICATION","For x=2,5,8 the corresponding y-values are 7,17.5,28. Prove the relationship is proportional and write its equation."),
("REASONING","A proportional graph contains the point (6,21). Explain why it must pass through the origin, find its gradient and predict y when x=10."),
("PROBLEM SOLVING","Printing 12 photographs costs 1,800 FCFA. Assuming direct proportion, find the cost of 30 photographs and state one assumption of the model.")],"answers":["k=2.5; y=35.","Each y/x=3.5, so y=3.5x.","Direct proportion has zero intercept; gradient 3.5; y=35.","4,500 FCFA; unit price must remain constant."]},
(2,3): {"source":"MYP2 Term 1 papers A/B","title":"Source-informed practice · Rates", "tasks":[
("FOUNDATION","A nurse counts 18 heartbeats in 15 seconds. Calculate the heart rate in beats per minute."),
("APPLICATION","A printer produces 96 pages in 4 minutes at a constant rate. Find its unit rate and the number of pages printed in 15 minutes."),
("REASONING","A bus travels 180 km in 2 h 15 min. Calculate its average speed and explain why dividing by 2.15 would be incorrect."),
("PROBLEM SOLVING","Rice costs 8,400 FCFA for 6 kg or 11,200 FCFA for 8.5 kg. Compare unit prices and quantify the saving per kilogram.")],"answers":["72 beats/min.","24 pages/min; 360 pages.","80 km/h; 15 min=0.25 h, not 0.15 h.","1,400 versus about 1,317.65 FCFA/kg; second saves about 82.35 FCFA/kg."]},
(2,10): {"source":"MYP2 Term 1 papers A/B","title":"Source-informed practice · Probability", "tasks":[
("FOUNDATION","A fair spinner has eight equal sectors numbered 1 to 8. Find the probability of an odd result and its complement."),
("APPLICATION","A maize seed germinates with probability 0.85. For 200 seeds, calculate the expected number that germinate and the expected number that do not."),
("REASONING","A die shows six on 38 of 180 rolls. Compare the relative frequency with the theoretical probability of a six and explain whether this proves the die is biased."),
("PROBLEM SOLVING","In a class of 40, 22 students join music, 18 join theatre and 9 join both. Find the probability that a randomly selected student joins neither group.")],"answers":["1/2 and 1/2.","170 germinate; 30 do not.","38/180=19/90≈0.211 versus 1/6≈0.167; this is evidence but not proof without more trials.","9/40."]},
(3,1): {"source":"Grade 8 MYP 3 assessment","title":"Source-informed practice · Real numbers", "tasks":[
("FOUNDATION","Classify √49, √18, 0.272727… and π using the most specific number set."),
("APPLICATION","Give an irrational number strictly between 4 and 5 and justify its position without a decimal approximation."),
("REASONING","Refute the claim ‘the product of two irrational numbers is always irrational’ using a counterexample and the definition of irrational number."),
("PROBLEM SOLVING","A square has side length √8 cm. Prove that its diagonal is rational and find its exact length.")],"answers":["√49=7 integer; √18 irrational; 0.272727…=3/11 rational; π irrational.","For example √17, because 16<17<25.","√2 and √2 are irrational but their product is 2, rational.","d=√(8+8)=√16=4 cm."]},
(3,2): {"source":"Grade 8 MYP 3 assessment","title":"Source-informed practice · Powers and scientific notation", "tasks":[
("FOUNDATION","Calculate (6×10^7)(3×10^-4), writing the answer in scientific notation."),
("APPLICATION","Calculate (4.8×10^-3)/(1.2×10^5), writing the answer in scientific notation."),
("REASONING","The sequence has U1=3 and Un+1=Un/2. Write its first five terms and derive an explicit formula."),
("CHALLENGE","Compare 2^30 and 8^10 without evaluating either whole number. Explain your conclusion using exponent laws.")],"answers":["1.8×10^4.","4×10^-8.","3,3/2,3/4,3/8,3/16; Un=3(1/2)^(n-1).","They are equal because 8^10=(2^3)^10=2^30."]},
(4,12): {"source":"Grade 9 MYP 4 assessment","title":"Source-informed practice · Statistics I", "tasks":[
("FOUNDATION","Goals in 12 matches were 2,0,3,1,2,4,2,1,0,3,2,4. Find mode, median, range and exact mean."),
("APPLICATION","Seven daily rainfalls are 12,14,15,15,16,18,22 mm. Find mean, median and IQR. Add an eighth value of 64 mm and recalculate all three measures."),
("REASONING","For the rainfall data, let the eighth value be x≥22. Express the new mean in terms of x and explain why the median and IQR remain constant."),
("CHALLENGE","P1={2,4,6,8}, P2=x+10 and P3=3x. Given μ1=5 and σ1=√5, find the means and standard deviations of P2 and P3, then generalise for w=ax+b, a>0.")],"answers":["Mode 2; median 2; range 4; mean 2.","Original: mean16, median15, IQR4. With64: mean22, median15.5, IQR5.5.","Mean=(112+x)/8; ordered middle positions and quartile positions are unchanged for x≥22.","P2: μ=15,σ=√5. P3: μ=15,σ=3√5. Generally μw=aμx+b and σw=aσx."]},
(4,12.1): {"source":"Grade 9 MYP 4 assessment","title":"Source-informed practice · Statistics II", "tasks":[
("FOUNDATION","Daily electricity use for 40 homes is grouped: 0≤E<4:8, 4≤E<8:15, 8≤E<12:11, 12≤E<16:6. Estimate the mean."),
("APPLICATION","A batch has volumes 496,498,500,502,504 mL with frequencies 1,2,4,2,1. Calculate population mean and standard deviation."),
("REASONING","A grouped estimate uses class midpoints. Explain why it need not equal the mean of the raw data and how narrower classes can affect accuracy."),
("PROBLEM SOLVING","Courier times are 18,19,21,22,22,23,25,26,76 min. Compare mean and median with and without 76, then recommend a typical-time measure.")],"answers":["Estimated mean 7.5 kWh.","μ=500 mL; σ=√4.8≈2.19 mL.","All values in a class are represented by one midpoint; narrower classes usually reduce possible approximation error.","All: mean28, median22. Without76: mean22, median22; use median when retaining the genuine outlier in audit data."]},
(5,4): {"source":"Grade 10 MYP 5 sequence assessments","title":"Source-informed practice · Sequences and series I", "tasks":[
("FOUNDATION","A sequence has un=3n²−2n+4. Calculate u1,u3 and u8."),
("APPLICATION","A linear sequence begins 46,39,32,25,… Derive un, find which term equals −45, and state the first negative term."),
("REASONING","An arithmetic sequence has u5=23 and u12=58. Find u1,d and S20."),
("CHALLENGE","A geometric sequence has u2=−24 and u5=192. Find r,u1 and un; determine whether −3072 is a term.")],"answers":["u1=5,u3=25,u8=180.","un=53−7n; −45 is u14; first negative is u8=−3.","d=5,u1=3,S20=1,010.","r=−2,u1=12,un=12(−2)^(n−1); −3072=u9."]},
(5,4.1): {"source":"Grade 10 MYP 5 sequence assessments","title":"Source-informed practice · Sequences and series II", "tasks":[
("FOUNDATION","Find n and the exact sum of 5+11+17+…+119."),
("APPLICATION","Find n and the exact sum of 320+160+80+…+5."),
("REASONING","A sequence has partial sums Sn=3n²+4n. Use un=Sn−S(n−1) to derive un and prove the sequence is arithmetic."),
("CHALLENGE","u1=5 and u(n+1)=3un−4. Let vn=un−2. Prove vn is geometric and derive an explicit formula for un.")],"answers":["n=20; S20=1,240.","n=7; S7=635.","u1=7 and un=6n+1; common difference6.","v(n+1)=3vn, v1=3, so vn=3^n and un=3^n+2."]}
}
