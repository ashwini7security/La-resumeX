var DEBUG = false 
 
    /* Autofills the passed dropdown object with contents based on it's name
      
       For day, month and year, fills with values.
       For courses, fills with degrees.
    */
    function fillOptions(o)
    {
        //o is the object in which options are to be filled

        //if options are already filled in there, we ain't gonna process it! performance :B
        if (o.children.length>1) 
        {
            return false;
        }
        
        switch (o.getAttribute('datatype'))
        {
                case 'month':
                    var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
          
                    for (var i =0;i<12;i++)
                        //o.innerHTML += "<option>"+months[i]+"</option>";
                    {
                        var option=document.createElement("option");
                        option.text=months[i];
                        option.value=months[i];
                        o.add(option,null)
                    }
                    break;
        
                case 'date':
                    for (var i =1;i<=31;i++)
                    //o.innerHTML += "<option>"+months[i]+"</option>";
                    {
                         var option=document.createElement("option");
                         option.text=i;
                         option.value=i;
                         o.add(option,null)
                    }
                    break;

                case 'year':
                    if((o.prevElementSibling)&&(o.previousElementSibling.value=="")) o.previousElementSibling.focus()
                    var d = new Date(); //so that we get a dynamic year :)

                    if(o.id.split('_')[0] == 'birthdate')
                        { var i=d.getFullYear()-60; var j=(d.getFullYear()-18);} // need to be min 18 yrs old..!!
                    else
                        {var i=d.getFullYear()-18; j=d.getFullYear()+2;}

                    for (;i<=j;i++)
                    //o.innerHTML += "<option>"+months[i]+"</option>";
                    {
                         var option=document.createElement("option");
                         option.text=i;
                         option.value=i;
                         o.add(option,null)

                    }
                    break;

                case 'strongAreas':
                case 'weakAreas':
                    var h=new Array('programming','database','os','web','packages','areasofinterest');
                    for( var i=0;i<h.length;i++)
                    {
                        c=document.getElementById(h[i]).children; //LI's

                        for(var j=0;j<c.length;j++)
                        {
                            if(c[j].children[0].value)
                            {
                                var option = document.createElement("option");
                                option.text=c[j].children[0].value
                                    o.add(option,null)
                            }
                        }

                    }
                    opt = o.options ; 
                    
                    if(opt.length  == 0) 
                        debug ('Please enter either of your software skill sets or Areas of interest to proceed');
                    break;
                default:
                    debug("Hey what to do with " + o.getAttribute('datatype'));
    } 
}     
/*
//DUMP CODE -- decide on removal


        else  if (o.name == 'course-g')
        {
          var course=new Array('BCA','BCS','BSc','BE','B.Tech', 'BBA','B.Com');
            for (var i =0;i<course.length;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=course[i];
                 o.add(option,null)
            }
        } 
          else  if (o.name == 'course-pg')
        {
          var course=new Array('MSc(CA) SEM I','MSc(CA) SEM II','MSc(CA) SEM III','MSc(CA) SEM IV','MBA(IT) SEM I','MBA(IT) SEM II','MBA(IT) SEM III','MBA(IT) SEM IV');
            for (var i =0;i<course.length;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=course[i];
                 o.add(option,null)
            }
        } 
*/

 /* changes the sibling fields to suit the current value of the passed object.
    
    For Months, changes the Day according to the capacity of the month.
    For the Appearing/Result Awaiting, disables the marks field.
   
    TODO: for leap year, it should make February right.
 */
function change(o)// Date and other fields dependency Checking.
 {
     id0=o.id.split('_')[0];
     id1=o.id.split('_')[1];
     id2=o.id.split('_')[2];
     prev=o.previousElementSibling;

     if (id0 == 'marks')
     {
      //debug(o.value);
      //we disable the Marks and OutOf elements for such times
      if (o.value == 'Appearing' || o.value =='Result Awaiting') 
      { 
         //debug('selecting ' + id0+'_'+'marks'+'_'+id2);
         marksEl = document.getElementById(id0+'_marks_'+id2); //select the corresponding marks element 

         marksEl.value=o.value;
         marksEl.disabled=true;
         marksEl.setAttribute('datatype','string')
  
         outofEl = document.getElementById(id0+'_outof_'+id2); //select the corresponding outof element 
         outofEl.value=o.value;
         outofEl.disabled=true;
         outofEl.setAttribute('datatype','string')
         
       // o.parentNode.removeChild(o.previousElementSibling);
      }
      else //if it is NOT appearing or Result Awaiting then, enable the Marks and OutOf elements
      {
         marksEl = document.getElementById(id0+'_marks_'+id2); //select the corresponding marks element 
         marksEl.disabled=false;
         marksEl.setAttribute('datatype','float')

         outofEl = document.getElementById(id0+'_outof_'+id2); //select the corresponding outof element 
         outofEl.disabled=false;
         outofEl.setAttribute('datatype','float')

         marksEl.focus();
      }
     }
     else if (id1 =='month')
     {
         if (prev.value=="")
             prev.focus();
         if (o.value =='Feb')
             if((prev.value=='30')||(prev.value=='31'))
             {
                 prev.value='28';
                 prev.focus();
             }
          if((o.value == 'April')||(o.value =='June')||(o.value =='Sept')||(o.value =='Nov'))
              if(prev.value=='31')
              {
                  prev.value='30';
                  prev.focus();
              }
            
     }
      else if (id1 =='date')
     {
         
         if (o.nextElementSibling.value =='Feb')
             if((o.value=='30')||(o.value=='31'))
             {
                o.value='28';
                o.focus();
             }
          if((o.nextElementSibling.value == 'April')||(o.nextElementSibling.value =='June')||(o.nextElementSibling.value =='Sept')||(o.nextElementSibling.value =='Nov'))
              if(o.value=='31')
              {
                  o.value='30';

                  o.focus();
              }
     }
 }

 function createDates(o) // adds another monthyear field. This concats the value of date, months and year and puts in one monthyear hidden field. so that it can be processes easyli while subitting.
 {
  debug('creating dates for ' + o.id);
  var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
  
  var id=o.id.split('_');
  var hidden=document.createElement('input')
  hidden.type="hidden";
  hidden.setAttribute('datatype','monthyear');
 
  if (id[1].indexOf("year")==-1) // for other fields - when called by onSubmitValidator
      return "alfa"
  else if(id[1].indexOf('year')==0) // for birthdate
      id[1] = 'monthyear'
  else
      id[1]=id[1].substr(0,id[1].indexOf("year"))+"monthyear"; // start_montheyar or endmonthyear.
  if (o.selectedIndex < 0 )
     return "unfilled"

  hidden.name=id.join("_");
  hidden.id=hidden.name;
  debug("We created an hidden el with id "+hidden.id + " and name "+ hidden.name);

  H=document.getElementById(hidden.name); // H = hidden only. if it already exists, then change existing instead fof creating a new one.

  
  // Set the value of monthyear as the date, month and year, if any. else set ot t 01,Jan,1990.
  if(!o.value)
      o.value = "2011"

  if ((o.previousElementSibling) && (o.previousElementSibling.id.indexOf('month') != -1)) // if it has a month to be concatenated,
      {
         var previousElementSiblingMonthKiValue=o.previousElementSibling.value 
        if ((o.previousElementSibling.previousElementSibling) && (o.previousElementSibling.previousElementSibling.id.indexOf('date') != -1)) // It also has a date.
          var previousElementSiblingDateKiValue=o.previousElementSibling.previousElementSibling.value
        else 
             previousElementSiblingDateKiValue="01"

      }
  else 
  { 
      var previousElementSiblingMonthKiValue="Feb"
      var previousElementSiblingDateKiValue="01"
  }
  
  newDate= previousElementSiblingDateKiValue+","+(months.indexOf(previousElementSiblingMonthKiValue)+1) + "," + o.value
  hidden.value=newDate;
  debug("We created a date called "+hidden.name+" with value " +hidden.value);
  if (H)
      {
      /* SUPER CODE to make hidden fields name properly and id properly preety! :)  --- by Apoorva*/
      H.value = hidden.value
      H.name = hidden.name
      H.id = hidden.id;
      }
  else    
    { 
      o.parentNode.appendChild(hidden);
    }
 }

/* check whether all fields in a row which are dependent on each other, are either fully filled or either fully empty. reports error on partially filled */
function dependencyCheck()
{
   var valid = true;
   var currentElement
   //take all rows -- all dependent fileds MUST be in the same TRs
   tr = document.getElementsByTagName('tr');
   
   a: for (var i=0;i<tr.length;i++)
   {
        input = tr[i].getElementsByTagName('input');
        select = tr[i].getElementsByTagName('select')
        textarea = tr[i].getElementsByTagName('textarea')

        l = textarea.length + select.length + input.length;
        filled = 0;
        
        for (var j = 0;j<input.length;j++)
            {
                currentElement = input[j]
                if(input[j].type == 'button') { l--;continue};
                if (input[j].type == 'hidden')
                {
                    l-- ; continue;
                }
                if (input[j].value != "") filled ++;
            }
              
         for (var j = 0;j<select.length;j++)
           {
                currentElement = select[j];
                if (select[j].selectedIndex >= 0) filled++
           }
           
        for (var j=0;j<textarea.length;j++)
            {
             currentElement = textarea[j];
             if (textarea[j].value !="" ) filled++
            }
        if(filled !=0 && l != filled) {valid = false; break a;}
    }
    if (!valid)
        highlightError(currentElement,!valid,'dependency')
    return valid

    
}
/* do all kinds of things necessary to know whether this form won't create server-side errrors. PLEASE */
function onSubmitValidator()
{
    if(!dependencyCheck()) return false;

    select_fields = document.getElementsByTagName('select'); //for cases like DOB

    // check select fields

    /* 1. mandatory select should be done.
       2. if dependent fields are filled, this should be filled.
    */
    for (var i=0;i<select_fields.length; i++)
    {
        if (select_fields[i].getAttribute('mandatory') == 'true')
        {
           if (select_fields[i].value == '' || select_fields[i].selectedIndex == -1)
           {
                reason = "mandatory";
                highlightError(select_fields[i],true,reason)
                return false;
           }
        }
        highlightError(select_fields[i],false,"")
        //IF WE EVER CHOOSE TO VALIDATE SELECTs
        //is_valid = validate(select_fields[i]);
        //priorly called concat
        createDates(select_fields[i]);
        //select_fields[i].name = select_fields[i].id
    }

    //now check input fields
    input_fields = document.getElementsByTagName('input');
    
    for (var i=0;i<input_fields.length;i++)
    {
     
     //we don't process disabled, hidden and button input elements
     if (input_fields[i].disabled == true ||  input_fields[i].type == 'button')
     {
                continue; //we don't want to touch such fields!
     }

     if (input_fields[i].type == 'hidden')
     {
         debug('we got an hidden field'); 
         is_valid = validate(input_fields[i]);
    
         //if not, get out.
         if (is_valid == false)
         {
             return is_valid;
         }
         continue;
     }
     //is this field mandatory ?

     if (input_fields[i].getAttribute('mandatory') == 'true')
     { 
            //do mandatory check.
           if (input_fields[i].value == '')
            {
                 reason = "mandatory";
                 highlightError(input_fields[i],true,reason);
                  //if not, get out.
                 return false;
            }
      }
     
     //is this field valid ? -- do validity checking
     is_valid = validate(input_fields[i]);
     debug('we got '+ is_valid + ' for the field '+ input_fields[i].id);
    
     //if not, get out.
     if (is_valid == false)
         return is_valid;
     else //everything seems ok, does this field have a proper id we can put in the name ?
     {
         // we need a name for each field that is to be stored
         //whether it's mandatory or not, we need to replace it with proper name
         //everything is good with this field now replace it's name with it's id.
        if ((input_fields[i].id != '' || input_fields[i].id != null) && (input_fields[i].value != '' || input_fields[i].value != null))
         {
           debug('changing name from ' + input_fields[i].name + ' to ' + input_fields[i].id);
           input_fields[i].name = input_fields[i].id    
         }
      }
   }
    
    //now check textarea fields
    textarea_fields = document.getElementsByTagName('textarea'); //for cases like Career Objective

    for (var i=0; i<textarea_fields.length; i++)
    {
        //is this field mandatory ?
        if (textarea_fields[i].getAttribute('mandatory') == 'true')
        {
           //does it have a value ?
           if (textarea_fields[i].value == '')
           {
                reason = "mandatory";
                highlightError(textarea_fields[i],true,reason)
                return false;
           }
        }
            

        //is this field valid ?
        //will check validations.
        //will also do dependency checking. --- UPDATE: nopes, dependency checking is now done seperately for all in the beginning of this validator
        is_valid = validate(textarea_fields[i]);
        if (is_valid == false)
        {
         debug("textarea "+is_valid);
         return is_valid;
        }
        else
        {
            //whether it's mandatory or not, we need to replace it with proper name so that it can be processed and stored
            //everything is good with this field now replace it's name with it's id.
            //TODO: Determine whether the value blank checking and null checking should be really done here ? Because we may like to submit some things as explicitly blank maybe...
            if ((textarea_fields[i].id != '' || textarea_fields[i].id != null) && (textarea_fields[i].value != '' || textarea_fields[i].value != null))
            {
                  textarea_fields[i].name = textarea_fields[i].id    
            }
        }
   }
    debug("We are valid ??" + is_valid);
    document.getElementById('allok').value = 1;
    
    
    f = document.getElementById('info_form');
    debug("Original action is " + f.action);
    debug("we are setting it to " + f.getAttribute('original_action'));
    f.action = f.getAttribute('original_action');
    debug('All OK! Now submitting the form');
    return true;
}

function highlightError(field, yesorno, reason)
{
    //take the field and it's style
    styleClasses = field.getAttribute('class');

    if (styleClasses) //this checks for blank and null value both 
        highlightClassPosition = styleClasses.indexOf('invalid_data'); 
    else //not uses styleClasses variable as it can be null. 
        highlightClassPosition = -1;

    //if we have to hihglight it,
    if (yesorno == true)
    {
       
        //was this priorly highlighted ? if no, do it
        if (highlightClassPosition == -1)
        {
               //is this a dependency check and hence the row needs to be fully highlighted  ?
               if (reason=='dependency')
               {
                    var rowID = 'tr_'+ field.id.split('_')[0] + '_'+field.id.split('_')[2];
                    debug("highlighting row " + rowID);
                    //document.getElementById(rowID).setAttribute('class',styleClasses + ' invalid_data');
               }
               else
               {
                    field.setAttribute('class',styleClasses + ' invalid_data');
               }
        }            
        //else,
    }
    else //if we have to unHighlight it,
    {
         //was this priorly highlighted ? 
        if (highlightClassPosition >= 0)
        {
                //-1 because we are taking from back
                classes_without_invalid_mark = styleClasses.slice(0,-1*highlightClassPosition);
                field.setAttribute('class',classes_without_invalid_mark);
        }            
    }
    // if a reason was given
    reasonArray = ['NaN','decimal_length','mandatory','numeric','dependency','email']
    messageArray = ['It should be a number.','It should be in the format 999999.999','It is a mandatory field.','It should be a +ve number.','All the items in the section must be filled.',' email not filled properly']
    if (reason != '')
    {
               //priorly called debugmsg
               fieldname = field.id.split('_')
               //now that we know validity, mark so visually and attributely
               //and tell the user
               if (field.getAttribute('desc'))
               {
                   fieldname[1] = field.getAttribute('desc');
               }
               if (fieldname.length > 2 ) //and there is more than one component in the name of the element
               {
                   alert(fieldname[1] + ' in the ' + fieldname[0] + ' section is invalid.\n'+messageArray[reasonArray.indexOf(reason)]);
               }
               else if (fieldname.length == 2)
               {
                   alert(fieldname[0] + ' ' + fieldname[1] + ' in Getting Started section is invalid.\n' + messageArray[reasonArray.indexOf(reason)]);
               }
               else
               {
                   alert(fieldname[0] + ' is invalid.\n' + messageArray[reasonArray.indexOf(reason)]);
               }
               
               //now bring us in spotlight!
               //TODO: find out a way to retrieve the parent tab of the element and call it's select() method 
               field.focus();
    }
}


/* check the dependency of a given field. */
/*function dependencyCheck(field)
{
    var tables = new Array('marks','workex','certification','projects','academic','extracurricular')
    
    //dependency checking -- if content is filled and the month-year isn't OR if month-year is filled and content isn't.
        debug('inside dependancy' + field.id)
        a=field.id.split('_')[0]
        if (tables.indexOf(a)>=0)
        {
            o=field.parentNode.parentNode.children;
            if (field.selectedIndex == -1)
               var field_was_filled = false;
            else
               var field_was_filled = true;
            debug(field_was_filled)
            for(var j=0;j<o.length;j++)
            {
                
                for (var k=0;k<o[j].children.length;k++)
                {
                   debug(o[j].children[k].value) 
                    if ((o[j].children[k].type == 'hidden') ||(o[j].children[k].disabled == true)) continue;
                    if ((o[j].children[k].tagName=="INPUT") || (o[j].children[k].tagName=="TEXTAREA")) 
                    {
                        if (field_was_filled)
                        {
                            if (o[j].children[k].value=="")
                                valid = false 
                        }
                         else
                         {
                            if(o[j].children[k].value !="")
                                valid = false;
                         }
                    }
                    else if (o[j].children[k].tagName == 'SELECT')
                    {
                        if (((field_was_filled) && (o[j].children[k].selectedIndex==-1))|| ((!field_was_filled) && (o[j].children[k].selectedIndex>0)))
                            valid = false                                                                        
                    }
                    else continue;
                    if (!valid)
                           { highlightError(field,true,'dependency'); return false;}
                }

            } 
        }
    return true;
}
*/

function debug(msg)
{
    if (DEBUG)
        alert(msg);
}

/* validates the data inside the passed field 
   currently in rudimentary state and will be expanded for all further.
*/
function validate(field)
{
   name = field.id.split('_'); 
   value = field.value;
   validateFor = field.getAttribute('datatype');
   valid = true;
   reason = '';
   switch (validateFor)
   {
        case 'float':
                   debug('i am in float');
                   parts = value.split('.');
                   if (parts.length == 1)
                       validateFor = 'numeric';
                   else
                   {
                       if ((parts.length != 2) || (isNaN(parts[0])) || (isNaN(parts[1])))
                       {
                           valid = false;
                           reason = 'NaN';
                       }
                       else
                       {
                            if ((parts[1].length > 4) || (parts[0].length > 6) || (value.length > 10))
                             {
                                valid = false;
                                reason = 'decimal_length';
                             }
                            else
                             {
                                valid = true;
                             }
                       }
                       highlightError(field,!valid,reason);
                       //break only when are we done fully addition.
                       break;
                    }
                    //we aren't breaking when the type is numeric
        case 'numeric':
                   debug('i am numeric');
                   if ((isNaN(value)) || (parseInt(value) < 0))
                   {
                      highlightError(field,true,"numeric");
                      valid = false;
                   }
                   else {valid = true; highlightError(field,false,"");}
                   break;
        case 'email':
                   debug('i am email'); // from w3chools
                    var atpos=value.indexOf("@");
                    var dotpos=value.lastIndexOf(".");
                    if ((atpos<1) || (dotpos<atpos+2) || (dotpos+2 >= value.length))
                      {
                         reason ="email"
                         valid =  false;
                      }
                    else
                      {
                            valid = true;
                      }
                    highlightError(field,!valid,reason);
                   //regexp = 'email ka regexp';
                   break;
         case 'monthyear':
                    debug ('value is ' + value);
                    parts = value.split(',');
                    if ((parseInt(parts[0]) >= 1 && parseInt(parts[0]) <= 31) && (parseInt(parts[1]) >= 1) && (parseInt(parts[1]) <= 12) && (parts[2] != ''))
                    {
                        valid = true;
                    }
                    else
                    {
                        valid = false;
                        //it's invalid, now we need to focus and highlight on the right field
                        id = field.id.split('_');
                        if (id[1].indexOf('monthyear') == 0)
                        {
                            id[1] = 'year';
                            
                        }
                        else
                        {
                            id[1] = id[1].substr(0,id[1].indexOf("monthyear"))+"year"; // start_montheyar or endmonthyear.
                        }
                        f = document.getElementById(id);
                        //to be on safe side 
                        createDates(f);

                        highlightError(f,!valid,'invalid_date');
                     }
                //WARNING: Samar added the break statement below because he thought it should be here :P 
                break; 
        case 'string': //only chars, spaces and parantheses and hyphen allowed...eg Full Name
               valid = true
               debug('i am string');
               break;
    }
 
    //if found invalid, stop right here.
    if (!valid)
        return false;
 
    switch (field.tagName)
    {
            case 'select':
            case 'SELECT':
//                     valid = dependencyCheck(field);
                        valid =true
                     
                    break;
            case 'input':
            case 'INPUT':
                       valid = true; 
                     break;
            case 'TEXTAREA':
            case 'textarea':
                     valid =true;
                     debug('i am in textarea');
                     break;
    }
   return valid;
}
function remove(o)
{
    // IF extra fields can be entered as blank, then students have write to remove all their pre-wriiten fields
    if (o.tagName=='TD')
    {
        p=o.parentNode;
        tid = p.id.split('_')
        firstSibling = p.parentNode.children[1];
        if(firstSibling == p) // if we want to delete the first row, 
           { 
            if (firstSibling.nextElementSibling)// incase there are other elements also, then put their ID as this ID.
                   {
                       firstSibling.nextElementSibling.id = tid[0];
                   }
           // else :- this is the inly element, then it;l be processed later.
           }
         else // its not hte first row to be deelting, then skip.
             firstSibling.id = tid[0] // for safety sake.. can be skipped.


        debug(p.parentNode.childElementCount)
        if(p.parentNode.childElementCount == 2) // because for Table, one child is The head. TH tags wla row
           {
               p.id = tid[0];  // to rename its ID as the main one. so that it can be "add another"ed
               // for each kind of eleemnt, change the Id to one. and value to blank
               a = p.getElementsByTagName('textarea'); 
               for (var i =0;i<a.length;i++)
                   {
                     id = a[i].id.split('_')
                     id[2]=1
                     a[i].id=id.join('_');
                     a[i].value = "";
                   }
               a = p.getElementsByTagName('input'); // remove the input type = hidden and retain the value of the remove button
               for (var i =0;i<a.length;i++)
                   {
                    if (a[i].type == 'hidden')
                        a[i].parentNode.removeChild(a[i])
                    else if (!a[i].type=="button")
                    { 
                        id=a[i].id.split('_')
                        id[2]=1;
                        a[i].id = id.join('_');
                        a[i].value = "";
                    }
                   }
               a = p.getElementsByTagName('select'); // remove all the option elemetns of the select button. 
               for(var i = 0;i<a.length;i++)
                   {
                        id = a[i].id.split('_');
                        id[2]=1;
                        a[i].id = id.join('_');
                        while(a[i].firstChild)
                            a[i].removeChild(a[i].firstChild)
                   }

                return false;
               
            }
        
        p.parentNode.removeChild(p) // of its NOT the only child, then remove the entire row.
    }
    else // same for LI types of input.
    {
        if (o.parentNode.childElementCount == 1)
        {
           
            a = o.getElementsByTagName('input');
               for (var i =0;i<a.length;i++)
                  { 
                    id = a[i].id.split('_');
                    i[2]=1;
                    a[i].id=id.join('_');
                    if (a[i].type != 'button')
                       a[i].value = "";
                  }

            return false;
        }
        o.parentNode.removeChild(o)
    }    
}    
       
   
