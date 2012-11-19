      
var all_fields; //used for storing all obj references to all fields that need any kind of processing

    /* Autofills the passed dropdown object with contents based on it's name
      
       For day, month and year, fills with values.
       For courses, fills with degrees.
    */
    function fillOptions(o)
    {
        //if options are already filled in there, we ain't gonna process it! performance :B
                if (o.children.length>1) 
                {
                    return false;
                }
    
        if (o.name == 'month')
        {
            var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
          
            for (var i =0;i<12;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=months[i];
                 o.add(option,null)

            }
        }
        else if(o.name == 'date')
        {
             for (var i =1;i<=31;i++)
            //o.innerHTML += "<option>"+months[i]+"</option>";
            {
                 var option=document.createElement("option");
                 option.text=i;
                 o.add(option,null)

            }
        }
        else if(o.name == 'year')
            {
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
                 o.add(option,null)

            }
           } 
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
        else if (o.name == "strongAreas" || o.name == "weakAreas" )
        {
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
           if(opt.length  == 0) alert ('Please enter either of your software skill sets or Areas of interest to proceed');
        }
    }
     
    

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
      //alert(o.value);
      //we disable the Marks and OutOf elements for such times
      if (o.value == 'Appearing' || o.value =='Result Awaiting') 
      { 
         //alert('selecting ' + id0+'_'+'marks'+'_'+id2);
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

 function concat(o) // adds another monthyear field. This concats the value of date, months and year and puts in one monthyear hidden field. so that it can be processes easyli while subitting.
 {
  var months=new Array('Jan','Feb','Mar','April','May','June','July','Aug','Sept','Oct','Nov','Dec');
  
  id=o.id.split('_');
  hidden=document.createElement('input')
  hidden.type="hidden";
  if (id[1].indexOf("year")==0) // forbirthdate
      id[1]="monthyear"
  else
      id[1]=id[1].substr(0,id[1].indexOf("year"))+"monthyear"; // start_montheyar or endmonthyear.
  
  hidden.name=id.join("_");
  hidden.id=hidden.name;

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
  if (H)
      H.value=hidden.value
  else    
      o.parentNode.appendChild(hidden);

 }

/* check whether mandatory values are filled or not */
function mandatoryCheck()
{ 
    //checks all those fields who have a mandatory attribute;

    input_fields = document.getElementsByTagName('input');
    select_fields = document.getElementsByTagName('select'); //for cases like DOB
    textarea_fields = document.getElementsByTagName('textarea'); //for cases like Career Objective

    all_fields = [input_fields,select_fields,textarea_fields]; //the total set of elements that we we want to check for mandatoriness 

    for (var j=0;j<all_fields.length;j++)
    {
        fields = all_fields[j]; //select the set of fields.
        
        for (var i=0; i<fields.length;i++)
        {
            if (fields[i].getAttribute('type') == 'hidden' || fields[i].type == 'button')
            {
                continue; //we don't want to touch such fields!
            }

            if (fields[i].getAttribute('mandatory') == 'true')
            {

             var field_name = fields[i].id; //because a field may or may not have a name but will always hv an ID
        
             //a=fields[i].name.split('_')[0]
             /* is the field enabled and still it's value is not entered */
             if ((fields[i].value=="")&&(input_fields[i].disabled==false) )
             {
               alertmsg = field_name.split('_')
               //now that we know validity, mark so visually and attributely
               //and tell the user

               styleClass = (fields[i].getAttribute('class') == null ? ' ' : fields[i].getAttribute('class')) ;
               fields[i].setAttribute('class',styleClass + ' invalid_data');
               
               if (alertmsg.length>1) //and there is more than one component in the name of the element
               {
                   alert(alertmsg[1] + ' in the ' + alertmsg[0] + '  section is not filled');
               }
               else
               {
                   alert(alertmsg[0] + ' is not filled!');
               }
               
               //TODO: find out a way to retrieve the parent tab of the element and call it's select() method 
               fields[i].focus();
               return false;
             }
             else //if found valid, clear any existing invalidity reference!
             {
                styleClass = fields[i].getAttribute('class');
                if (styleClass != null)
                {
                    x = fields[i].getAttribute('class').indexOf('invalid_data');
                    class_without_invalid_mark = fields[i].getAttribute('class').slice(0,-1*x);
                    fields[i].setAttribute('class',class_without_invalid_mark);
                }
    
                
             }
           }
           //whether it's mandatory or not, we need to replace it with proper name
           //everything is good with this field now replace it's name with it's id.
           if ((fields[i].id != '' || fields[i].id != null) && (fields[i].value != '' || fields[i].value != null))
           {
              //alert('setting name of ' + fields[i].name + ' to ' + fields[i].id);
              if (fields[i].tagName != 'select')
              fields[i].name = fields[i].id; // we dont need to do this for select. ebcause we have monthyear. and of dependency checking fails, then the name also gets changed. which creates a problem later on.
           }
       }
  }
   
     
    var tables = new Array('marks','workex','certification','projects','academic','extracurricular')
    
    //dependency checking -- if content is filled and the month-year isn't OR if month-year is filled and content isn't.
    select=document.getElementsByTagName('select');
    for (var i=0;i<select.length;i++)
    {
        a=select[i].id.split('_')[0]
        if (tables.indexOf(a)>=0)
        {
            o=select[i].parentNode.parentNode.children;
            if (select[i].value)
               var filled=true;
            else
                var filled = false;
        
            for(var j=0;j<o.length;j++)
            {
                
                for (var k=0;k<o[j].children.length;k++)
                {
                    
                    if ((o[j].children[k].tagName=="INPUT" || o[j].children[k].tagName=="SELECT" || o[j].children[k].tagName=="TEXTAREA") && ((filled && !o[j].children[k].value)|| (!filled && o[j].children[k].value)))
                    {
                        alertmsg=o[j].children[k].id.split('_');
                        alert('Check your '+ alertmsg[0] +'  entry...' + alertmsg[1] +' is not filled properly'); return false;
                    }
                }

            } 
        }
    } 
    //alert('returning true')
    return true;
}

/* replaces all name attributes of all input, select and textarea elements with their ids so that they can be successfull when the form is submitted. */
function changeName()
{
    //check mandatoriness!
    x = mandatoryCheck();
    //alert(x);
    if (!x)
    {
        //alert('since mandatory check failed, we are returning false');
        return false;
    }
    //alert('mandatory check was passed...going ahead');

    select_fields = document.getElementsByTagName('select');
    try
    {
        for (var i=0;i<select_fields.length;i++)
        {
            //for all elements who are named 'month' OR 'year'
           if (select_fields[i].id.indexOf('date') >= 0 || select_fields[i].id.indexOf('year') >= 0 || select_fields[i].id.indexOf('month') >= 0)
           {
               //we havee to concat all the year fields with 
               //their corresponding month and day AND create a new hidden element for submission

               //do this only an year field...
               if (select_fields[i].id.indexOf('year')>=0)
               {
                   concat(select_fields[i])
               }
               //now render this select field as unsuccessful by removing it's name -- it won't be submitted.
               //thee shall deem them unsuccessfull
                 //debugger;
               select_fields[i].name=null;
               continue;
           }
           //since this is now handled by mandatoryCheck itself :-)
/*           else //this isn't a date or month or year field
           {
               select_fields[i].name=select_fields[i].id;
               //Check whether it's filled or not ?
               if (select_fields[i].value=="")
               {
                    alert("hey, " + select_fields[i].id + " is not filled");
                    select_fields[i].focus();
                    return false;
               } 
           }*/
        }
        //alert('done processing select_fields');

       //now tell in the form submission the secret
        document.getElementById('allok').value = 0;
        //return confirm("Do you want to really submit the form ?");
        return true;

    }
    catch (e)
    {
        alert(e);
    }
}

/*
  used to remove instances of an extra field.
*/
function remove(o)
{
    // IF extra fields can be entered as blank, then students have write to remove all their pre-wriiten fields
    if (o.tagName=='TD')
    {
        p=o.parentNode;
        alert(p.parentNode.childElementCount)
        if(p.parentNode.childElementCount == 2) // because for Table, one child is The head. TH tags wla row
           {
               // for each kind of eleemnt, change the Id to one. and value to blank
               a = p.getElementsByTagName('textarea'); 
               for (var i =0;i<a.length;i++)
                   {
                     id =    a[i].id.split('_')
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
       
   
