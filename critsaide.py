import argparse
from pprint import pprint
from TLO.TLO import TLO

def cmd_parse(cmd):
	if len(cmd) == 1:
		return cmd
	else:
		_type = cmd[0]
		_name = ' '.join(cmd[1:len(cmd)])
		return [_type, _name]

def main():
	parser = argparse.ArgumentParser(prog='PROG', description='This program interfaces with CRITS \
		allowing the user to get, add, and delete TLOs as well as establish relationships \
		between existing TLOs and adding TLOs to current Campaigns. Be sure to set the correct hosting IP under "IP" \
		in the config.json file.',\
		usage='[-h] [-a TLO_type] [-g TLO_type NAME] [-d TLO_type NAME] [-r TLO_type NAME] [-c TLO_type NAME] [-q]')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-a', '--add', nargs='+', metavar='', help='add crits TLO')
	group.add_argument('-g', '--get', nargs='+', metavar='',help='get TLO from crits')
	group.add_argument('-d', '--delete', nargs='+', metavar='',help='delete crits TLO')
	group.add_argument('-r', '--relationship', nargs='+', metavar='',help='establish relationship between two existing TLOs')
	group.add_argument('-c', '--campaign', nargs='+', metavar='', help='add TLO item to campaign')
	group.add_argument('-q', '--quit', action='store_true', help='Quit program')

	parser.print_help()
	while True:
	    TLO.DB_refresh() #update config
	    cmd = raw_input('$: ')
	    try:
	        args = parser.parse_args(cmd.split())
	    except SystemExit:
	        # trap argparse error message
	        continue
	    
	    if args.add != None:
	        cmd = cmd_parse(args.add)
	        if (len(cmd) == 1) and (cmd[0] in TLO.approved):
	        	response = TLO.add_TLO(cmd[0])
	        	if response != None:
	        		if 'url' in response:
	        			print 'upload success! URL: %s' % response['url']
	        		else:
	        			print 'upload failed: %s' % response['message']
	        	else:
	        		print 'upload failed'
	        else:
	        	print 'ERROR: TLO type required'
	        	continue

	    elif args.get != None:
	        cmd = cmd_parse(args.get)
	        if len(cmd) > 1:
	        	try:
		        	TLO_get = TLO(cmd[0], cmd[1])
		        	result = TLO_get.get()
		        	if result != None:
		        		pprint(result)
		        	else:
		        		print 'No %s named %s' % (TLO_get.type, TLO_get.name)
		        except ValueError:
		        	print 'ERROR: not a TLO type'
		        	continue
	        else:
	        	print 'ERROR: TLO type AND name required'
	        	continue
	    
	    elif args.delete != None:
	        cmd = cmd_parse(args.delete)
	        if len(cmd) > 1:
	        	try:
		        	TLO_delete = TLO(cmd[0], cmd[1])
		        	result = TLO_delete.delete()
		        	if result.deleted_count == 1:
		        		print '%s document deleted: ' % (TLO_delete.name)
		        	else:
		        		print 'No %s named %s' % (TLO_delete.type, TLO_delete.name)
	        	except ValueError:
		        	print 'ERROR: not a TLO type'
		        	continue
	        else:
	        	print 'ERROR: TLO type AND name required'
	        	continue

	    elif args.relationship != None:
	        cmd = cmd_parse(args.relationship)
	        if len(cmd) > 1:
	        	try:
	        		Left_TLO = TLO(cmd[0], cmd[1])
	        		ans = cmd_parse(raw_input('Enter next TLO type and name: ').split())
	        		if len(ans) > 1:
	        			try:
	        				Right_TLO = TLO(ans[0], ans[1])
	        				result = Left_TLO.relationship(Right_TLO)
	        				if result != False:
	        					if result != None:
	        						print 'success! relationship established between %s and %s' % (Left_TLO.name, Right_TLO.name)
	        					else:
	        						print 'ERROR: relationship failed'
	        				else:
	        					print 'relationship already established'
	        			except ValueError:
				        	print 'ERROR: not a TLO type'
				        	continue
	        	except ValueError:
		        	print 'ERROR: not a TLO type'
		        	continue
	        else:
	        	print 'ERROR: TLO type AND name required'
	        	continue

	    elif args.campaign != None:
	    	cmd = cmd_parse(args.campaign)
	        if len(cmd) > 1:
	        	try:
		        	TLO_campaign = TLO(cmd[0], cmd[1])
		        	new_campaign = raw_input('Enter campaign name: ')
		        	result = TLO_campaign.add_campaign(new_campaign)
		        	if result != False:
		        		if result != None:
		        			print 'success! %s added to %s' % (TLO_campaign.name, new_campaign)
		        		else:
		        			print '%s already linked to %s' % (TLO_campaign.name, new_campaign)
		        	else:
		        		print '%s does not exist' % TLO_campaign.name
		        except ValueError:
		        	print 'ERROR: not a TLO type'
		        	continue
	        else:
	        	print 'ERROR: TLO type AND name required'
	        	continue

	    elif args.quit:
	        print 'Goodbye'
	        break

if __name__ == '__main__':
	main()