import sys
import os
import csv

def main():
	clin_filename = sys.argv[1]
	clin_detailed_filename = sys.argv[2]
	maf_filename = sys.argv[3]

	if os.path.exists(clin_filename) and os.path.exists(maf_filename) and os.path.exists(clin_detailed_filename):
		clin_file = open(clin_filename, 'rU')
		clin_detailed_file = open(clin_detailed_filename, 'rU')
		maf_file = open(maf_filename, 'rU')
	else:
		print 'bad filenames'
		sys.exit(2)

	sample_data = {}

	# process general clin file
	clin_reader = csv.DictReader(clin_file, dialect = 'excel-tab')
	for line in clin_reader:
		if line['CANCER_TYPE'] == 'Colorectal Cancer' or line['CANCER_TYPE'] == 'Anal Cancer':
			sample_data[line['SAMPLE_ID']] = {'CANCER_TYPE':line['CANCER_TYPE'], 'CANCER_TYPE_DETAILED':line['CANCER_TYPE_DETAILED'], 'GENE_PANEL':line['GENE_PANEL']}

	clin_detailed_reader = csv.DictReader(clin_detailed_file, dialect = 'excel-tab')
	for line in clin_detailed_reader:
		sample_data[line['SAMPLE_ID']]['MSI_STATUS'] = line['MSI_STATUS']

	maf_reader = csv.DictReader(maf_file, dialect = 'excel-tab')
	for line in maf_reader:
		variant = {}
		sid = line['Tumor_Sample_Barcode']
		if sid in sample_data:
			variant['Variant_Type'] = line['Variant_Type']
			variant['Hugo_Symbol'] = line['Hugo_Symbol']
			if sample_data[sid].get('VARIANT', '')  == '':
				sample_data[sid]['VARIANT'] = [variant]
			else:
				sample_data[sid]['VARIANT'].append(variant)

	print len(sample_data)
	for sample, data in sample_data.iteritems():
		print sample
		print data

if __name__ == '__main__':
	main()