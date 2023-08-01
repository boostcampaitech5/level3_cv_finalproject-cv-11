import React from 'react';
import './Footer.css';
import {Button} from "reactstrap";
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <div className='footer-container'>
      <div className='footer-links'>
        <div className='footer-link-wrapper'>
          <div className='footer-link-items'>
            <h2>About Fakey</h2>
            <a href='https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11'>Github</a>
            <a href='https://www.notion.so/boostcampait/CV-11-Personalized-deepfake-5bb96df20d2b4fb0b5bcaaefb9246344'>Notion</a>
          </div>
          <div className='footer-link-items'>
            <h2>Contact Us</h2>
            <Link to='/about'>Contact</Link>
          </div>
        </div>
        <div className='footer-link-wrapper'>
          <div className='footer-link-items'>
            <h2>Aivengers</h2>
            <a href='https://www.notion.so/AIvengers-93c2f674ed434dcfb31a2179767b331f?pvs=4'>Team Notion</a>
            <a href='https://github.com/boostcampaitech5/level2_objectdetection-cv-11'>Detection</a>
            <a href='https://github.com/boostcampaitech5/level2_cv_datacentric-cv-11'>Data-centric</a>
            <a href='https://github.com/boostcampaitech5/level2_cv_semanticsegmentation-cv-11'>Segmentation</a>
          </div>
          {/* <div className='footer-link-items'>
            <h2>SNS</h2>
            <Link to='/'>Instagram</Link>
            <Link to='/'>Facebook</Link>
            <Link to='/'>Youtube</Link>
          </div> */}
        </div>
      </div>
      <section className='social-media'>
        <div className='social-media-wrap'>
          <div className='footer-logo'>
            <Link to='/' className='social-logo'>
              Fakey &nbsp;
              <i className="fab fa-contao"/>
            </Link>
          </div>
          <small className='website-rights'>Aivengers © 2023</small>
          <div className='social-icons'>
            <Link
              className='social-icon-link facebook'
              to='/'
              target='_blank'
              aria-label='Facebook'
            >
              <i className='fab fa-facebook-f' />
            </Link>
            <Link
              className='social-icon-link instagram'
              to='/'
              target='_blank'
              aria-label='Instagram'
            >
              <i className='fab fa-instagram' />
            </Link>
            <Link
              className='social-icon-link youtube'
              to='/'
              target='_blank'
              aria-label='Youtube'
            >
              <i className='fab fa-youtube' />
            </Link>
            <Link
              className='social-icon-link twitter'
              to='/'
              target='_blank'
              aria-label='Twitter'
            >
              <i className='fab fa-twitter' />
            </Link>
            <Link
              className='social-icon-link twitter'
              to='/'
              target='_blank'
              aria-label='LinkedIn'
            >
              <i className='fab fa-linkedin' />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Footer;