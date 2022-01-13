'''
------------------------------------------------------------------------------------------------------------------------
This workflow is used to build the trees from the aligned gene sequences.



------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------
Author: Oscar Wrisberg
Date: 7/12/2021
------------------------------------------------------------------------------------------------------------------------
'''

from os import O_SYNC
from gwf import Workflow
import os.path
# import math
# import glob

gwf = Workflow()

##########################################################################################################################
# #########################################---- Copying alignments ----###################################################
# ########################################################################################################################

def partitioner(path_in, gene):
    """Copying alignments from the manual alignment folder to the treebuilding folder and creating partition files"""
    inputs = ["/home/owrisberg/Coryphoideae/work_flow/09_manual_edit/02_edited_alignments/"+gene+"_aligned.fasta"]
    outputs = [path_in+gene+"_aligned.part.txt",path_in+gene+"_aligned.clean.fasta"]
    options = {'cores': 1, 'memory': "5g", 'walltime': "00:20:00", 'account':"Coryphoideae"}

    spec = """

	source activate treebuilder_env

	#Removing files used for last round of tree searching
	cd {path_in}
	[-f {gene}_aligned_part.txt] && rm {gene}_aligned_part.txt || echo "{gene}_aligned_part.txt does not exist"
	[-f {gene}_aligned_clean.fasta] && rm {gene}_aligned_clean.fasta || echo "{gene}_aligned_clean.fasta does not exist"

	#Copying manually edited genes
	cd /home/owrisberg/Coryphoideae/work_flow/09_manual_edit/02_edited_alignments
	cp {gene}_aligned.fasta ../04_alignments_for_trees

	#Going to folder with data
	cd {path_in}
    
	#The partitioner should produce 2 files for each gene
	#one file called gene_aligned_part.txt which is the partitioning file
	#another called gene_aligned_clean.fasta which are just the sequences without the exons

	python3 /home/owrisberg/Coryphoideae/github_code/coryphoideae_species_tree/partitioner.py --smoother 10 --{gene}


    """.format(path_in = path_in, gene = gene)

    return (inputs, outputs, options, spec)


# ########################################################################################################################
# #############################################---- IQ-tree ----#############################################################
# ########################################################################################################################

# def iq_tree(path_in, gene, ):
#     """Using Iq-tree to produce trees for each gene"""
#     inputs = [path_in+gene+"_aligned_part.txt"]
#     outputs = []
#     options = {'cores': 20, 'memory': "10g", 'walltime': "04:00:00", 'account':"Coryphoideae"}

#     spec = """

# 	#IQtree genetree search
# 	for f in *_part.txt; do (cp $f ${f/_part.txt}_clean.part); done

# 	cp {gene} 

# 	for f in *_aligned_clean.fasta
# 	do
# 		if [[$f -a ]] && [["${f/_aligned_clean_fasta}_aligned_part.txt" -a ]]
# 		then 
# 			ls *clean.fasta | parallel -j 6 iqtree2 -s {} -T AUTO -ntmax 4 -p {.}.part -B 1000
# 		else
# 			echo "Skipping gene" $f
# 			continue
# 		fi
# 	done


# 	#Clean up and file transfer
# 		for f in *_aligned_clean.fasta 
# 	do
# 		mv ${f/clean.fasta}clean.part.treefile /home/owrisberg/Coryphoideae/work_flow/11_tree_building/01_genetrees/${f/clean.fasta}part.txt.tre
# 		mv ${f/clean.fasta}part.txt* /home/owrisberg/Coryphoideae/work_flow/11_tree_building/01_genetrees #This works
# 	 	mv ${f/_aligned_clean.fasta}.fasta 05_alignments_used_in_trees
# 	 	rm ${f}
# 	done

# 	""".format(path_in = path_in, gene = gene)

#     return (inputs, outputs, options, spec)


# ########################################################################################################################
# #############################################---- IQ-tree ----#############################################################
# ########################################################################################################################



########################################################################################################################
######################################################---- RUN ----#####################################################
########################################################################################################################
genes = ["EGU105032175","EGU105032229","EGU105032337","EGU105032379","EGU105033063","EGU105033626","EGU105034121","EGU105034616","EGU105034893","EGU105034993","EGU105035046","EGU105035196","EGU105035203","EGU105035462","EGU105035555","EGU105035989","EGU105036031","EGU105036385","EGU105036774","EGU105037749","EGU105037800","EGU105037890","EGU105037902","EGU105037930","EGU105037938","EGU105038008","EGU105038036","EGU105038098","EGU105038099","EGU105038100","EGU105038110","EGU105038114","EGU105038118","EGU105038123","EGU105038179","EGU105038201","EGU105038228","EGU105038234","EGU105038245","EGU105038252","EGU105038310","EGU105038382","EGU105038400","EGU105038419","EGU105038431","EGU105038499","EGU105038513","EGU105038571","EGU105038580","EGU105038603","EGU105038631","EGU105038680","EGU105038693","EGU105038720","EGU105038747","EGU105038794","EGU105038832","EGU105038882","EGU105038986","EGU105038988","EGU105039013","EGU105039062","EGU105039067","EGU105039082","EGU105039099","EGU105039101","EGU105039107","EGU105039121","EGU105039164","EGU105039178","EGU105039221","EGU105039236","EGU105039255","EGU105039282","EGU105039298","EGU105039313","EGU105039403","EGU105039431","EGU105039449","EGU105039460","EGU105039480","EGU105039494","EGU105039501","EGU105039512","EGU105039542","EGU105039587","EGU105039595","EGU105039609","EGU105039660","EGU105039685","EGU105039690","EGU105039699","EGU105039763","EGU105039783","EGU105039809","EGU105039822","EGU105039925","EGU105039947","EGU105039957","EGU105039962","EGU105040073","EGU105040088","EGU105040099","EGU105040114","EGU105040115","EGU105040125","EGU105040139","EGU105040185","EGU105040186","EGU105040189","EGU105040206","EGU105040207","EGU105040242","EGU105040281","EGU105040302","EGU105040308","EGU105040359","EGU105040368","EGU105040426","EGU105040452","EGU105040462","EGU105040530","EGU105040583","EGU105040667","EGU105040675","EGU105040684","EGU105040690","EGU105040700","EGU105040756","EGU105040758","EGU105040813","EGU105040837","EGU105040842","EGU105040850","EGU105040851","EGU105040863","EGU105040887","EGU105040914","EGU105040918","EGU105040922","EGU105040957","EGU105040970","EGU105041055","EGU105041100","EGU105041117","EGU105041125","EGU105041127","EGU105041133","EGU105041179","EGU105041182","EGU105041189","EGU105041217","EGU105041246","EGU105041283","EGU105041337","EGU105041353","EGU105041650","EGU105041657","EGU105041665","EGU105041680","EGU105041687","EGU105041710","EGU105041807","EGU105041816","EGU105041872","EGU105041902","EGU105041903","EGU105041929","EGU105041933","EGU105041982","EGU105042090","EGU105042113","EGU105042128","EGU105042147","EGU105042168","EGU105042205","EGU105042290","EGU105042307","EGU105042323","EGU105042329","EGU105042368","EGU105042422","EGU105042525","EGU105042558","EGU105042560","EGU105042584","EGU105042633","EGU105042644","EGU105042651","EGU105042664","EGU105042722","EGU105042781","EGU105042808","EGU105042820","EGU105042873","EGU105042965","EGU105043011","EGU105043037","EGU105043042",
"EGU105043061","EGU105043069","EGU105043119","EGU105043155","EGU105043160","EGU105043164","EGU105043193","EGU105043320","EGU105043338","EGU105043374","EGU105043419","EGU105043430","EGU105043469","EGU105043485","EGU105043499","EGU105043601","EGU105043633","EGU105043666","EGU105043685","EGU105043686","EGU105043730","EGU105043786","EGU105043816","EGU105043827","EGU105043926","EGU105043975","EGU105044063","EGU105044120","EGU105044133","EGU105044174","EGU105044182","EGU105044183","EGU105044203","EGU105044252","EGU105044281","EGU105044307","EGU105044309","EGU105044350","EGU105044378","EGU105044400","EGU105044407","EGU105044445","EGU105044446","EGU105044481","EGU105044588","EGU105044613","EGU105044614","EGU105044668","EGU105044676","EGU105044710","EGU105044758","EGU105044844","EGU105044846","EGU105044854","EGU105044885","EGU105044893","EGU105044896","EGU105044978","EGU105044982","EGU105044983","EGU105044984","EGU105045005","EGU105045043","EGU105045070","EGU105045078","EGU105045094","EGU105045099","EGU105045102","EGU105045137","EGU105045148","EGU105045232","EGU105045248","EGU105045254","EGU105045282","EGU105045310","EGU105045358","EGU105045367","EGU105045424","EGU105045464","EGU105045467","EGU105045489","EGU105045507","EGU105045509","EGU105045514","EGU105045520","EGU105045529","EGU105045544","EGU105045640","EGU105045658","EGU105045703","EGU105045726","EGU105045732","EGU105045760","EGU105045782","EGU105045788","EGU105045820","EGU105045827","EGU105045828","EGU105045835","EGU105045898","EGU105045932","EGU105045946","EGU105046030","EGU105046050","EGU105046056","EGU105046099","EGU105046103","EGU105046147","EGU105046168","EGU105046245","EGU105046297","EGU105046360","EGU105046387","EGU105046393","EGU105046401","EGU105046449","EGU105046454","EGU105046456","EGU105046503","EGU105046518","EGU105046530","EGU105046549","EGU105046559","EGU105046562","EGU105046574","EGU105046630","EGU105046632","EGU105046696","EGU105046735","EGU105046766","EGU105046786","EGU105046827","EGU105046875","EGU105046918","EGU105047024","EGU105047029","EGU105047253","EGU105047288","EGU105047293","EGU105047342","EGU105047357","EGU105047362","EGU105047379","EGU105047385","EGU105047395","EGU105047433","EGU105047434","EGU105047446","EGU105047519","EGU105047533","EGU105047546","EGU105047553","EGU105047578","EGU105047585","EGU105047597","EGU105047621","EGU105047644","EGU105047662","EGU105047689","EGU105047751","EGU105047777","EGU105047790","EGU105047907","EGU105047916","EGU105047922","EGU105047940","EGU105047945","EGU105047970","EGU105048009","EGU105048015","EGU105048028","EGU105048054","EGU105048056","EGU105048129","EGU105048130","EGU105048137","EGU105048159","EGU105048182","EGU105048199","EGU105048300","EGU105048357","EGU105048410","EGU105048474","EGU105048476","EGU105048479","EGU105048484","EGU105048486","EGU105048493","EGU105048527","EGU105048541","EGU105048581","EGU105048612","EGU105048694","EGU105048725","EGU105048751","EGU105048796","EGU105048839","EGU105048867","EGU105048886","EGU105048898",
"EGU105048909","EGU105048915","EGU105048926","EGU105048961","EGU105048968","EGU105049007","EGU105049016","EGU105049020","EGU105049025","EGU105049052","EGU105049097","EGU105049274","EGU105049312","EGU105049318","EGU105049360","EGU105049426","EGU105049539","EGU105049543","EGU105049583","EGU105049690","EGU105049729","EGU105049737","EGU105049761","EGU105049827","EGU105049882","EGU105049902","EGU105049903","EGU105049934","EGU105049947","EGU105050012","EGU105050023","EGU105050036","EGU105050058","EGU105050114","EGU105050126","EGU105050202","EGU105050207","EGU105050328","EGU105050344","EGU105050362","EGU105050366","EGU105050383","EGU105050387","EGU105050404","EGU105050432","EGU105050450","EGU105050521","EGU105050532","EGU105050644","EGU105050670","EGU105050680","EGU105050681","EGU105050682","EGU105050831","EGU105050841","EGU105050853","EGU105050854","EGU105050961","EGU105050970","EGU105050972","EGU105051087","EGU105051146","EGU105051156","EGU105051188","EGU105051345","EGU105051362","EGU105051366","EGU105051373","EGU105051391","EGU105051395","EGU105051403","EGU105051481","EGU105051499","EGU105051503","EGU105051560","EGU105051564","EGU105051582","EGU105051614","EGU105051677","EGU105051704","EGU105051726","EGU105051740","EGU105051748","EGU105051764","EGU105051795","EGU105051802","EGU105051821","EGU105051823","EGU105051832","EGU105051847","EGU105051857","EGU105051860","EGU105051870","EGU105051891","EGU105051924","EGU105051953","EGU105051985","EGU105052035","EGU105052070","EGU105052170","EGU105052178","EGU105052304","EGU105052307","EGU105052346","EGU105052351","EGU105052386","EGU105052389","EGU105052394","EGU105052428","EGU105052446","EGU105052476","EGU105052483","EGU105052492","EGU105052495","EGU105052527","EGU105052529","EGU105052538","EGU105052552","EGU105052573","EGU105052580","EGU105052623","EGU105052650","EGU105052694","EGU105052704","EGU105052739","EGU105052743","EGU105052750","EGU105052771","EGU105052804","EGU105052818","EGU105052849","EGU105052855","EGU105052865","EGU105052888","EGU105052944","EGU105052947","EGU105052956","EGU105053006","EGU105053055","EGU105053059","EGU105053079","EGU105053105","EGU105053124","EGU105053130","EGU105053136","EGU105053172","EGU105053204","EGU105053227","EGU105053263","EGU105053403","EGU105053422","EGU105053426","EGU105053457","EGU105053465","EGU105053468","EGU105053482","EGU105053549","EGU105053642","EGU105053654","EGU105053735","EGU105053747","EGU105053770","EGU105053835","EGU105053848","EGU105053866","EGU105053889","EGU105053901","EGU105053932","EGU105053961","EGU105053969","EGU105053974","EGU105053980","EGU105054002","EGU105054124","EGU105054130","EGU105054153","EGU105054204","EGU105054280","EGU105054293","EGU105054405","EGU105054435","EGU105054440","EGU105054455","EGU105054457","EGU105054469","EGU105054478","EGU105054486","EGU105054498","EGU105054529","EGU105054534","EGU105054595","EGU105054649","EGU105054653","EGU105054668","EGU105054723","EGU105054765","EGU105054786","EGU105054827","EGU105054845","EGU105054864",
"EGU105054891","EGU105054896","EGU105054898","EGU105054924","EGU105054930","EGU105054936","EGU105054948","EGU105054972","EGU105055008","EGU105055015","EGU105055023","EGU105055024","EGU105055030","EGU105055047","EGU105055052","EGU105055065","EGU105055072","EGU105055075","EGU105055077","EGU105055090","EGU105055093","EGU105055098","EGU105055114","EGU105055115","EGU105055130","EGU105055144","EGU105055157","EGU105055201","EGU105055283","EGU105055433","EGU105055438","EGU105055490","EGU105055499","EGU105055507","EGU105055550","EGU105055569","EGU105055621","EGU105055634","EGU105055664","EGU105055709","EGU105055755","EGU105055761","EGU105055771","EGU105055800","EGU105055862","EGU105055873","EGU105055883","EGU105055889","EGU105055908","EGU105055912","EGU105055913","EGU105056032","EGU105056091","EGU105056151","EGU105056269","EGU105056287","EGU105056289","EGU105056313","EGU105056323","EGU105056365","EGU105056382","EGU105056393","EGU105056460","EGU105056468","EGU105056469","EGU105056496","EGU105056530","EGU105056534","EGU105056539","EGU105056654","EGU105056662","EGU105056684","EGU105056688","EGU105056714","EGU105056726","EGU105056817","EGU105056848","EGU105056881","EGU105056943","EGU105056960","EGU105056998","EGU105057013","EGU105057015","EGU105057019","EGU105057074","EGU105057090","EGU105057110","EGU105057130","EGU105057194","EGU105057235","EGU105057256","EGU105057335","EGU105057357","EGU105057553","EGU105057579","EGU105057634","EGU105057666","EGU105057669","EGU105057721","EGU105057742","EGU105057795","EGU105057841","EGU105057912","EGU105057919","EGU105057941","EGU105058078","EGU105058081","EGU105058083","EGU105058094","EGU105058107","EGU105058131","EGU105058170","EGU105058175","EGU105058180","EGU105058202","EGU105058237","EGU105058241","EGU105058245","EGU105058326","EGU105058366","EGU105058377","EGU105058418","EGU105058469","EGU105058499","EGU105058547","EGU105058556","EGU105058567","EGU105058576","EGU105058582","EGU105058592","EGU105058598","EGU105058614","EGU105058633","EGU105058682","EGU105058683","EGU105058687","EGU105058702","EGU105058723","EGU105058731","EGU105058781","EGU105058798","EGU105058802","EGU105058808","EGU105058863","EGU105058889","EGU105058890","EGU105058894","EGU105058904","EGU105058918","EGU105058989","EGU105058990","EGU105059003","EGU105059008","EGU105059023","EGU105059035","EGU105059042","EGU105059054","EGU105059108","EGU105059112","EGU105059113","EGU105059126","EGU105059131","EGU105059138","EGU105059176","EGU105059186","EGU105059193","EGU105059276","EGU105059342","EGU105059366","EGU105059367","EGU105059381","EGU105059441","EGU105059453","EGU105059458","EGU105059479","EGU105059480","EGU105059490","EGU105059570","EGU105059573","EGU105059575","EGU105059587","EGU105059594","EGU105059612","EGU105059624","EGU105059636","EGU105059639","EGU105059671","EGU105059853","EGU105059900","EGU105059996","EGU105060095","EGU105060589","EGU105061025","EGU105061385","EGU105061427",
"HEY1007","HEY1013","HEY1017","HEY1020","HEY1025","HEY1035","HEY1050","HEY1052","HEY1064","HEY110","HEY1119","HEY1168","HEY1171","HEY1197","HEY1201","HEY120","HEY122","HEY125","HEY12","HEY136","HEY139","HEY1484","HEY148","HEY1494","HEY14","HEY150","HEY1615","HEY164","HEY168","HEY17","HEY1801","HEY180","HEY1815","HEY182","HEY1842","HEY1854","HEY1877","HEY1901","HEY191","HEY194","HEY197","HEY1986","HEY201","HEY204e","HEY204s","HEY2056","HEY207","HEY215","HEY2164","HEY218","HEY21","HEY2238","HEY225","HEY226","HEY2291","HEY231","HEY2339","HEY2363","HEY2370","HEY2377","HEY237","HEY2388","HEY240","HEY2459","HEY245","HEY24","HEY250","HEY252e","HEY252p","HEY252s","HEY2550","HEY2561","HEY257","HEY267","HEY269","HEY277","HEY280","HEY281","HEY282","HEY290","HEY293","HEY296","HEY299","HEY305","HEY308","HEY310","HEY31","HEY323","HEY326","HEY32e","HEY32s","HEY332","HEY334","HEY340","HEY357","HEY360","HEY362","HEY363","HEY369","HEY378e","HEY378s","HEY38","HEY391","HEY392","HEY415","HEY417","HEY421","HEY429","HEY449","HEY464","HEY484","HEY490","HEY497","HEY4","HEY508",
"HEY514","HEY51","HEY52","HEY556","HEY563","HEY576","HEY581","HEY587","HEY604","HEY609","HEY61","HEY629","HEY630","HEY637","HEY673","HEY680","HEY703","HEY717","HEY727","HEY728","HEY732","HEY736","HEY740","HEY743","HEY757","HEY758","HEY762","HEY763","HEY785","HEY790","HEY793","HEY7","HEY807","HEY808","HEY822","HEY825","HEY82","HEY83","HEY84","HEY855","HEY856","HEY863","HEY872","HEY874","HEY883e","HEY883n","HEY886","HEY88","HEY897","HEY89","HEY938","HEY948","HEY94","HEY950","HEY958","HEY964","HEY977","HEY982","HEY985","HEY989"]


#Main workflow for trees
for i in range(len(genes)):
    #### Running Mafft
    gwf.target_from_template('Partition_'+genes[i], partitioner(gene = genes[i],
                                                        path_in = "/home/owrisberg/Coryphoideae/work_flow/09_manual_edit/04_alignments_for_trees"))

    