    # def import_encrypted(self):
    #     '''Function to import all pages of the origin file as a list (of lists) [list_pages(list_lines)].'''
        
    #     print('Importing all lines from the encoded file...')
    #     with open('./text/encoded.txt','rb') as fr:
    #         list_lines = fr.readlines()

    #     print('Structuring the data...')
    #     # w, h = 38,31
    #     # self.arr_lines = [['boba' for x in range(w)] for y in range(h)]
    #     arr_lines = []
    #     page, i = 0, 0
    #     for line in list_lines:
    #         if line.startswith(b'Page'):
    #             if i>9:
    #                 page = 10*int(chr(line[5]))+int(chr(line[6])) 
    #             else:
    #                 page = int(chr(line[5]))
    #             print('Accessing page', page,'...')
    #             i+=1
    #             continue
    #         self.arr_lines[page-1].append([line])

        # del self.arr_lines[0] 
        # for page in self.arr_lines:
        #     while(page[-1] == 'boba'):
        #         del page[-1]



    # def export_decrypted():
        # '''Writing the decoded text to another file, to prove that we are on the right path (we can encrypt and then decrypt strings)
        # We don't run this any more, as the script already gave a valid output once.'''

        # i = 1
        # print('Writing to text file...')
        # with open('./decoded.txt', 'w', encoding='utf-8') as fwrite:
        #     for array_page in arr_lines:
        #         fwrite.write(''.join(['Page',str(i)]))
        #         fwrite.write('\n')
        #         i +=1
        #         for bytes_line in array_page:
        #             decr_line = f.decrypt(bytes_line)
        #             fwrite.write(str(decr_line))
        #             fwrite.write('\n')
